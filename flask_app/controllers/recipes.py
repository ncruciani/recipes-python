from flask import render_template, redirect, request, session
from flask import flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    user = User.get_by_id({'id': session['user_id']})
    recipes = Recipe.get_all()
    return render_template("dashboard.html", user=user, recipes=recipes)


@app.route("/recipes/new")
def new_recipe():
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    return render_template("new_recipe.html")


@app.route("/recipes/new/process", methods=["POST"])
def create_recipe():
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under30': request.form['under30'],
        'user_id': session['user_id']
    }
    errors = Recipe.validate_recipe(data)
    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect("/recipes/new")
    id = Recipe.save(data)
    session['recipe_id'] = id
    flash("Recipe successfully created!", "success")
    return redirect("/dashboard")


@app.route("/recipes/<int:recipe_id>")
def view_recipe(recipe_id):
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    recipe = Recipe.get_by_id({'id': recipe_id})
    if not recipe:
        flash("Recipe not found.", "error")
        return redirect("/dashboard")
    return render_template("view.html", recipe=recipe)


@app.route("/recipes/edit/<int:recipe_id>")
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    recipe = Recipe.get_by_id({'id': recipe_id})
    if not recipe:
        flash("Recipe not found.", "error")
        return redirect("/dashboard")
    if recipe.creator.id != session['user_id']:
        flash("You are not authorized to edit this recipe.", "error")
        return redirect("/dashboard")
    return render_template("edit_recipe.html", recipe=recipe)



@app.route("/recipes/edit/process/<int:recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    recipe = Recipe.get_by_id({'id': recipe_id})
    if not recipe:
        flash("Recipe not found.", "error")
        return redirect("/dashboard")
    if recipe.creator.id != session['user_id']:
        flash("You are not authorized to edit this recipe.", "error")
        return redirect("/dashboard")
    form_data = {
        'id': recipe.id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under30': request.form['under30']
    }
    errors = Recipe.validate_recipe(request.form)
    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(f"/recipes/edit/{recipe.id}")
    
    
    Recipe.update(form_data)
    flash("Recipe successfully updated!", "success")
    return redirect("/dashboard")



@app.route("/recipes/destroy/<int:recipe_id>")
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        flash("Please log in to view this page.", "login")
        return redirect("/")
    recipe = Recipe.get_by_id({'id': recipe_id})
    if not recipe:
        flash("Recipe not found.", "error")
        return redirect("/dashboard")
    if recipe.creator.id != session['user_id']:
        flash("You are not authorized to delete this recipe.", "error")
        return redirect("/dashboard")
    Recipe.delete({'id': recipe.id})
    flash("Recipe successfully deleted!", "success")
    return redirect("/dashboard")
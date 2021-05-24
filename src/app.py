from flask import Flask, render_template, request, redirect, url_for, session, g
from models import select_pizza, create_connection, close_connection, select_pizza_by_id, insert_pizza, delete_pizza_by_id, select_ingr, update_pizza, update_ingr, select_ingr_change, delete_ingr_by_id, authoriz, insert_ingr, insert_new_order, select_pizza_by_id_zakaz, select_order_by_id, select_order, select_order_by_last_id, change_status_by_id, change_status_by_id_return, delete_order_by_id
import logging
import hashlib


app = Flask(__name__)
app.config["SECRET_KEY"] = "123"


logging.basicConfig(
    filename="log.txt",
    filemode="w",
    format='%(asctime)s -- %(name)s -- %(message)s',
    level=logging.DEBUG,
    )
logger = logging.getLogger(__name__)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        ses = request.form["username"]
        if authoriz(g.con, ses) == []:
            error = "Invalid username or password"
        elif authoriz(g.con, ses)[0][0] == hashlib.md5((request.form["password"]).encode('utf-8')).hexdigest():
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)


@app.route("/")
def index():
    pizzas = select_pizza(g.con)
    ingr = select_ingr(g.con)
    return render_template("index.html", pizzas=pizzas, ingr=ingr)

@app.route("/show_pizza/<int:pizza_id>")
def show_pizza(pizza_id):
    pizza = select_pizza_by_id(g.con, pizza_id)
    ingred = select_ingr(g.con)
    return render_template("show_pizza.html", pizza=pizza, ingred=ingred)


@app.route("/show_orders")
def show_orders():
    orders = select_order(g.con)
    return render_template("show_orders.html", orders=orders)


@app.route("/order/<int:order_id>", methods=("GET", "POST"))
def order(order_id):
    zakaz = select_order_by_id(g.con, order_id)
    return render_template("order.html", zakaz=zakaz)


@app.route("/show_pizza/<int:pizza_id>", methods=("POST", ))
def create_order(pizza_id):
    price = 0
    pizza_name = None
    description = []
    for item_info in request.form.items():
        if item_info[0] == "pizza_price":
            price += float(item_info[1])
        elif item_info[0].startswith("ingredient."):
            price += float(item_info[1])
            description.append(item_info[0].split(".")[-1])
        elif item_info[0] == "pizza_name":
            pizza_name = item_info[1]
    prices = str(price)
    price = prices.split(".")[0]
    ingr_des = ", ".join(description)
    ingr = select_pizza_by_id_zakaz(g.con, pizza_id)
    pizza_ingr = ingr[0]
    insert_new_order(g.con, pizza_name, pizza_ingr, ingr_des, price)
    order = select_order_by_last_id(g.con)
    return render_template("my_order.html", order=order)


@app.route("/add_ingr", methods=["GET", "POST"])
def add_ingr():
    error = None
    if request.method == "GET":
        return render_template("add_ingr.html")
    elif request.method == "POST":
        ingr_name = request.form["name"]
        ingr_price = request.form["price"]
        if ingr_price.isdigit():
            insert_ingr(g.con, ingr_name, ingr_price)
            return redirect(url_for("index"))
        else:
            error = "Incorrectly price"
    return render_template("add_ingr.html", error=error)


@app.route("/add_pizza", methods=["GET", "POST"])
def add_pizza():
    error = None
    if request.method == "GET":
        return render_template("add_pizza.html")
    elif request.method == "POST":
        pizza_name = request.form["pizza_name"]
        pizza_price = request.form["pizza_price"]
        pizza_description = request.form["pizza_description"]
        pizza_image = request.form["pizza_image"]
        if pizza_price.isdigit():
            insert_pizza(g.con, pizza_name, pizza_price, pizza_description, pizza_image)
            return redirect(url_for("index"))
        else:
            error = "Incorrectly price"
    return render_template("add_pizza.html", error=error)


@app.route("/change_pizza", methods=["POST"])
def change_pizza():
    pizza_name = request.form["pizza_name"]
    pizza_price = request.form["pizza_price"]
    pizza_description = request.form["pizza_description"]
    pizza_image = request.form["pizza_image"]
    pizza_id = int(request.form["pizza_id"])
    if pizza_price.isdigit():
        update_pizza(g.con, pizza_name, pizza_price, pizza_description, pizza_image, pizza_id)
        return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.route("/change_or_del_ingr", methods=["POST"])
def change_ingr():
    ingr_name = request.form["ingr_name"]
    ingr_price = request.form["ingr_price"]
    ingr_id = request.form["ingr_id"]
    if ingr_price.isdigit() and ingr_id.isdigit():
        update_ingr(g.con, ingr_name, ingr_price, ingr_id)
        return redirect(url_for("change_or_del_ingr_show"))
    return redirect(url_for("change_or_del_ingr_show"))


@app.route("/change_or_del_ingr")
def change_or_del_ingr_show():
    ingr = select_ingr_change(g.con)
    return render_template("change_or_del_ingr.html", ingr=ingr)


@app.route("/delete_pizza", methods=["POST"])
def delete_pizza():
    pizza_id = int(request.form["pizza_id"])
    delete_pizza_by_id(g.con, pizza_id)
    return redirect(url_for("index"))


@app.route("/change_status", methods=["POST"])
def change_status():
    order_id = int(request.form["order_id"])
    change_status_by_id(g.con, order_id)
    return redirect(url_for("show_orders"))


@app.route("/change_status_baked", methods=["POST"])
def change_status_baked():
    order_id = int(request.form["order_id"])
    change_status_by_id_return(g.con, order_id)
    return redirect(url_for("show_orders"))


@app.route("/delete_ingr", methods=["POST"])
def delete_ingr():
    ingr_id = request.form["ingr_id"]
    if ingr_id.isdigit():
        delete_ingr_by_id(g.con, ingr_id)
        return redirect(url_for("change_or_del_ingr_show"))
    return redirect(url_for("change_or_del_ingr_show"))


@app.route("/delete_prder", methods=["POST"])
def delete_order():
    order_id = request.form["order_id"]
    if order_id.isdigit():
        delete_order_by_id(g.con, order_id)
        return redirect(url_for("show_orders"))
    return redirect(url_for("show_orders"))



@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("index"))


@app.before_request
def before_request():
    g.con = create_connection()


@app.teardown_request
def teardown_request(exception):
    close_connection(g.con)


@app.errorhandler(500)
def internal_server_error(e):
    return "SORRY!", 500

from flask import Flask ,jsonify, make_response,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
from sqlalchemy import or_,and_
# import matplotlib.pyplot as plt
# import numpy as np
# from pylab import *


app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ycrhcrhfrcjqyz:7fd8060bfcdad4071b1495b4faf829e61550cb291535b465a402fb0fca64d29e@ec2-54-163-234-4.compute-1.amazonaws.com:5432/det2gahm246c0g'
db = SQLAlchemy(app)



def drawPlot(x,y):
    pass
    # n = 50
    # x =  np.array (x)
    # y = x *  np.array(y)
    # fig, ax = plt.subplots()
    # fit = np.polyfit(x, y, deg=1)
    # ax.plot(x, fit[0] * x + fit[1], color='red')
    # ax.scatter(x, y)
    # fig.show()


class UserJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'id': obj.id,
                'name': obj.name,
                'email': obj.email,
                'password': obj.password,
                'Role': obj.Role,
            }
        elif isinstance(obj, Products):
            return {
                'id': obj.id,
                'name': obj.name,
                'manufacture': obj.manufacture,
                'amount': obj.amount,
                'description': obj.description,
                'quantity': obj.quantity,
                'date': obj.date,
            }
        elif isinstance(obj, Store):
            return {
                'id': obj.id,
                'storeName': obj.storeName,
                'location': obj.location,
            }
        elif isinstance(obj, Sales):
            return {
                'id': obj.id,
                'saleDate': obj.saleDate,
                'quantity': obj.quantity,
                'stockSold': obj.stockSold,
                'totalAmount': obj.totalAmount,
                'storeID': obj.storeID,
                'productID': obj.productID,
            }
        return super(UserJSONEncoder, self).default(obj)


app.json_encoder = UserJSONEncoder


class User(db.Model):
    __tablename__ = 'userFlask'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))
    Role = db.Column(db.Boolean)

    def __init__(self, name, email, password, Role):
        # self.id  = id
        self.name = name
        self.email = email
        self.Role = Role
        self.password = password

    def __init__(self, data):
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.Role = data['Role']

    def __repr__(self):
        return '<User %r>' % self.name


class Products(db.Model):
    __tablename__ = 'ProductsFlask'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    name = db.Column(db.String(120))
    manufacture = db.Column(db.String(120))
    description = db.Column(db.String(120))
    amount = db.Column(db.Integer())
    quantity = db.Column(db.Integer(),nullable=True)
    date = db.Column(db.Date,nullable=True)

    def __init__(self, name, manufacture, description, amount,quantity,date):
        self.name = name
        self.manufacture = manufacture
        self.amount = amount
        self.description = description
        self.quantity = quantity
        self.date = date


    def __init__(self, data):
        self.name = data['name']
        self.manufacture = data['manufacture']
        self.amount = data['amount']
        self.description = data['description']
        self.quantity = data['quantity']
        self.date = data['date']

    def __repr__(self):
        return '<User %r>' % self.name


class Store(db.Model):
    __tablename__ = 'StoresFlask'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    storeName = db.Column(db.String(120))
    location = db.Column(db.String(120))


    def __init__(self, storeName, location):
        self.storeName = storeName
        self.location = location

    def __init__(self, data):
        self.storeName = data['storeName']
        self.location = data['location']


    def __repr__(self):
        return '<User %r>' % self.storeName


class Sales(db.Model):
    __tablename__ = 'SalesFlask'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    saleDate = db.Column(db.Date)
    quantity = db.Column(db.Integer())
    stockSold = db.Column(db.Integer())
    totalAmount = db.Column(db.Integer())
    storeID = db.Column(db.Integer,db.ForeignKey('StoresFlask.id'))
    productID = db.Column(db.Integer,db.ForeignKey('ProductsFlask.id'))

    def __init__(self, saleDate, quantity, stockSold, totalAmount,storeID,productID):
        # self.id  = id
        self.saleDate = saleDate
        self.quantity = quantity
        self.stockSold = stockSold
        self.totalAmount = totalAmount
        self.storeID = storeID
        self.productID = productID

    def __init__(self, data):
        self.saleDate = data['saleDate']
        self.quantity = data['quantity']
        self.totalAmount = data['totalAmount']
        self.stockSold = data['stockSold']

    def __init__(self):
         return None


    def __repr__(self):
        return '<User %r>' % self.productID

# db.create_all()

@app.route('/signup', methods = ['POST'])
def signup():
    try:
        email = request.form['email']
        name = request.form['name']
        role = request.form['Role']
        password = request.form['password']

    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Required parametes are missing OR Invalid Parameters'})
    else:
        if len(User.query.filter_by(email=email).all()) == 0:
                user = User(request.form)
                db.session.add(user)
                db.session.commit()
                return jsonify({'data': user, 'message': 'Sucessfully Registered', 'error': ''})
        return jsonify({'data': '', 'message': 'Failed', 'error': 'User with ' + email + ' Already registered'})


@app.route('/login', methods = ['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Parameters'})
    else:
        user = User.query.filter_by(email=email, password=password).all()
        if len(user) != 0:
            user = user[0]
            return jsonify({'data': user, 'message': 'Sucessfully Registered', 'error': ''})
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid email/Password'})

@app.route('/AddProduts', methods=['POST'])
def AddProduts():
        try:
            id = request.form['uid']
            name = request.form['name']
            manufacture = request.form['manufacture']
            description = request.form['description']
            amount = request.form['amount']
            quantity = request.form['quantity']
            date = request.form['date']

        except:
            return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Data/Parameters'})
        else:
            user = User.query.filter_by(id=id).all()
            if len(user) == 0:
                return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
            else:
                user = user[0]
                product = Products(request.form)
                db.session.add(product)
                db.session.commit()
                return jsonify({'data': product, 'message': 'Your report has been submitted sucessfully', 'error': ''})

@app.route('/getProducts/<int:id>/', methods=['GET'])
def getProducts(id):
    try:
        id = id
    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
    else:
        user = User.query.filter_by(id=id).all()
        if len(user) == 0:
            return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
        else:
            user = user[0]
            if user.Role == False:
                allProducts = Products.query.all()
                return jsonify({'data': allProducts, 'message': 'Sucessfull', 'error': ''})
            else:
                jsonify({'data': '', 'message': 'Failed', 'error': 'You have not permission to get products'})

@app.route('/editProduct', methods=['POST'])
def editProduct():
    try:
        uid = request.form['uid']
        pid = request.form['pid']
        name = request.form['name']
        manufacture = request.form['manufacture']
        description = request.form['description']
        amount = request.form['amount']
        quantity = request.form['quantity']
        date = request.form['date']

    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Data/Parameters'})
    else:
        user = User.query.filter_by(id = uid).all()
        if len(user) != 0:
            user = user[0]
            product = Products.query.filter_by(id=pid).all()
            if len(product) != 0:
                product = product[0]
                product.name = name
                product.manufacture = manufacture
                product.description = description
                product.amount = amount
                product.quantity = quantity
                product.date = date
                db.session.add(product)
                db.session.commit()
                return jsonify({'data': product, 'message': 'Sucessfully Updated', 'error': ''})
            else:
                return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid product id'})
        else:
            return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})


@app.route('/deleteProduct', methods=['DELETE'])
def deleteProduct():
    try:
        pid = request.form['pid']
        uid = request.form['uid']
    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Data/Parameters'})
    else:
        user = User.query.filter_by(id = uid).all()
        if len(user) != 0:
            user = user[0]
            product = Products.query.filter_by(id=pid).all()
            if len(product) != 0 :
                product = product[0]
                db.session.delete(product)
                db.session.commit();
                return jsonify({'data': '', 'message': 'Sucessfully Deleted', 'error': ''})
            else:
                return jsonify({'data': '', 'message': 'Failed', 'error': 'Product with pid = ' + pid + ' not available'})
        else:
            return jsonify({'data': '', 'message': 'Failed', 'error': 'User is not available with id  = ' + uid})

@app.route('/addStores', methods=['POST'])
def addStores():
    try:
        id = request.form['uid']
        storeName = request.form['storeName']
        location = request.form['location']

    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Data/Parameters'})
    else:
        user = User.query.filter_by(id=id).all()
        if len(user) != 0:
            store = Store(request.form)
            db.session.add(store)
            db.session.commit()
            return jsonify({'data': store, 'message': 'Sucessfully Registered', 'error': ''})
        return jsonify({'data': '', 'message': 'Failed', 'error': 'User with ' + id + ' not registered'})

@app.route('/getStores/<int:id>/', methods=['GET'])
def getStores(id):
    try:
        id = id
    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
    else:
        user = User.query.filter_by(id=id).all()
        if len(user) == 0:
            return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
        else:
            user = user[0]
            if user.Role == False:
                stores = Store.query.all()
                return jsonify({'data': stores, 'message': 'Sucessfull', 'error': ''}, )
            else:
                return  jsonify({'data': '', 'message': 'Failed', 'error': 'You have not permission to get products'})


@app.route('/AddSales', methods=['POST'])
def AddSales():
    try:
        pid = request.form['pid']
        sid = request.form['sid']
        aid = request.form['uid']
        saleDate = request.form['saleDate']
        quantity = request.form['quantity']
        stockSold = request.form['stockSold']

    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Data/Parameters'})
    else:
        user = User.query.filter_by(id=aid).all()
        if len(user) != 0:
            product = Products.query.filter_by(id=pid).all()
            store = Store.query.filter_by(id=sid).all()
            if len(product) != 0 :
                if len(store) != 0:
                    product = product[0]
                    store = store[0]
                    quantity = int(quantity)
                    if product.quantity >= quantity:
                        totalAmt = quantity * product.amount
                        product.quantity = product.quantity - quantity
                        db.session.add(product)
                        db.session.commit()
                        sale = Sales()
                        sale.storeID = sid
                        sale.productID = pid
                        sale.quantity = quantity
                        sale.saleDate = saleDate
                        sale.stockSold = stockSold
                        sale.totalAmount = totalAmt
                        db.session.add(sale)
                        db.session.commit()
                        return jsonify({'data': '', 'message': 'Sucessfully','error': 'Product with pid = ' + pid + ' added in Sales'})

                    else:
                        return jsonify({'data': '', 'message': 'Failed', 'error': 'Your desired quantity = ' + str(
                            quantity) + ' and available in stock is = ' + str(product.quantity)})
                else:
                    return jsonify({'data': '', 'message': 'Failed', 'error': 'Store with ' + sid + ' not available'})
            else:
                return jsonify({'data': '', 'message': 'Failed', 'error': 'Product with ' + pid + ' not available'})
        else:
            return jsonify({'data': '', 'message': 'Failed', 'error': 'User with ' + aid + ' not available'})


@app.route('/getSales/<int:id>/', methods=['GET'])
def getSales(id):
    try:
        id = id
    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
    else:
        user = User.query.filter_by(id=id).all()
        if len(user) == 0:
            return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
        else:
            user = user[0]
            if user.Role == False:
                data = []
                sales = Sales.query.all()
                for s in sales:
                    sname = Store.query.filter_by(id=s.storeID).all()
                    pname = Products.query.filter_by(id=s.productID).all()

                    data.append({'sale': s, 'productName': pname[0].name,
                                 'storeName':sname[0].storeName, 'storeLocation':sname[0].location})
                return jsonify({'data': data, 'message': 'Sucessfull', 'error': ''})

            else:
                return jsonify({'data': '', 'message': 'Failed', 'error': 'You have not permission to get Sales'})


@app.route('/getPredictSale', methods=['POST'])
def getPredictSale():
    try:
        id = request.form['uid']
        pid = request.form['pid']

    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
    else:
        user = User.query.filter_by(id=id).all()
        if len(user) == 0:
            return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
        else:
            user = user[0]
            if user.Role == False:
                product = Products.query.filter_by(id=pid).all()
                if len(product) != 0:
                    sale = Sales.query.filter_by(productID=pid).order_by('saleDate').all()
                    if len(sale) != 0:
                        salesAmmounts = [amt.totalAmount for amt in sale]
                        x = []
                        y = []
                        for index, salAmt in enumerate(salesAmmounts):
                            x.append(index + 1)
                            y.append(salAmt)
                        drawPlot(x, y)
                        print(x)
                        print(y)
                        return jsonify({'data': sale, 'message': 'Sucessfull', 'error': ''})
                    else:
                        return jsonify({'data': '', 'message': 'Failed', 'error': 'You have not sold this product yet'})
                else:
                    return jsonify(
                        {'data': '', 'message': 'Failed', 'error': 'Product with id = ' + pid + ' not available'})
            else:
                return jsonify({'data': '', 'message': 'Failed', 'error': 'You have not permission to get Sales'})



@app.route('/getPredictStore', methods=['POST'])
def getPredictStore():
    try:
        id = request.form['uid']
        sid = request.form['sid']

    except:
        return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
    else:
        user = User.query.filter_by(id=id).all()
        if len(user) == 0:
            return jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
        else:
            user = user[0]
            if user.Role == False:
                store = Store.query.filter_by(id=sid).all()
                if len(store) != 0:
                    sale = Sales.query.filter_by(storeID=sid).order_by('saleDate').all()
                    if len(sale) != 0:
                        salesAmmounts = [amt.totalAmount for amt in sale]
                        x = []
                        y = []
                        for index, salAmt in enumerate(salesAmmounts):
                            x.append(index + 1)
                            y.append(salAmt)
                        drawPlot(x, y)


                        print(x)
                        print(y)
                        return jsonify({'data': sale, 'message': 'Sucessfull', 'error': ''})
                    else:
                        return jsonify({'data': '', 'message': 'Failed', 'error': 'You have not sold this product yet'})
                else:
                    return jsonify(
                        {'data': '', 'message': 'Failed', 'error': 'Product with id = ' + sid + ' not available'})
            else:
                return jsonify({'data': '', 'message': 'Failed', 'error': 'You have not permission to get Sales'})


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Notfound' }),404)

if __name__ == '__main__':
    app.run()

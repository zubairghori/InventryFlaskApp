from flask import Flask ,jsonify, make_response,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
from sqlalchemy import or_,and_
# import matplotlib.pyplot as plt
# import numpy as np
# from pylab import *
from flask_cors import CORS, cross_origin
from flask.ext.bcrypt import Bcrypt
import jwt , datetime


app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lfeamxcqafgsfh:8e02a7f6660833a012e4021d5956462d7e84bf5c38c1761190e4e757f671badc@ec2-23-23-222-147.compute-1.amazonaws.com:5432/d6pffsqn0ti14a'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)



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
        self.password  = self.encrypt(password)

    def __init__(self, data):
        self.name = data['name']
        self.email = data['email']
        self.password = self.encrypt(data['password'])
        self.Role = data['Role']

    def __repr__(self):
        return '<User %r>' % self.name


    def encrypt(self,password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def decrypt(self,enteredPassword):
        return bcrypt.check_password_hash(self.password, enteredPassword)

    def generateToken(self):
        return jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=180) , 'id':self.id}, "secret",algorithm='HS256').decode()

    @staticmethod
    def verifyToken(token):
        return jwt.decode(token,"secret")['id']



class Products(db.Model):
    __tablename__ = 'ProductsFlask'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    name = db.Column(db.String(120))
    manufacture = db.Column(db.String(120))
    description = db.Column(db.String(120))
    amount = db.Column(db.Integer())
    quantity = db.Column(db.Integer(),nullable=True)
    date = db.Column(db.Date,nullable=True)
    userID  = db.Column(db.Integer,db.ForeignKey('userFlask.id'))

    def __init__(self, name, manufacture, description, amount,quantity,date,userID):
        self.name = name
        self.manufacture = manufacture
        self.amount = amount
        self.description = description
        self.quantity = quantity
        self.date = date
        self.userID = userID


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
    userID  = db.Column(db.Integer,db.ForeignKey('userFlask.id'))


    def __init__(self, storeName, location,userID):
        self.storeName = storeName
        self.location = location
        self.userID = userID

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
    userID  = db.Column(db.Integer,db.ForeignKey('userFlask.id'))

    def __init__(self, saleDate, quantity, stockSold, totalAmount,storeID,productID,userID):
        # self.id  = id
        self.saleDate = saleDate
        self.quantity = quantity
        self.stockSold = stockSold
        self.totalAmount = totalAmount
        self.storeID = storeID
        self.productID = productID
        self.userID = userID

    def __init__(self, data):
        self.saleDate = data['saleDate']
        self.quantity = data['quantity']
        self.totalAmount = data['totalAmount']
        self.stockSold = data['stockSold']

    def __init__(self):
         return None


    def __repr__(self):
        return '<User %r>' % self.productID

db.create_all()

@app.route('/signup', methods = ['POST'])
def signup():
    email = request.json['email']
    if len(User.query.filter_by(email=email).all()) == 0:
        user = User(request.json)
        db.session.add(user)
        db.session.commit()
        token = user.generateToken()
        return jsonify({'data': {"user": user, "token": token}, 'message': 'Sucessfully Registered', 'error': ''})
    return make_response(
        jsonify({'data': '', 'message': 'Failed', 'error': 'User with ' + email + ' Already registered'}), 409)


@app.route('/login', methods = ['POST'])
def login():
    try:
        email = request.json['email']
        password = request.json['password']
    except:
        return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Parameters'}), 404)
    else:
        user = User.query.filter_by(email=email).all()
        if len(user) != 0:
            user = user[0]
            if user.decrypt(enteredPassword=password) == True:
                token = user.generateToken()
                return jsonify({'data': {'user': user, 'token': token}, 'message': 'Sucessfully Login', 'error': ''})
            else:
                return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Password'}), 401)
        return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid email'}), 401)


@app.route('/AddProduts', methods=['POST'])
def AddProduts():
    try:
        token = request.headers['token']
    except:
        return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
    else:
        try:
            id = User.verifyToken(token=token)
        except:
            return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
        else:
            try:
                name = request.json['name']
                manufacture = request.json['manufacture']
                description = request.json['description']
                amount = request.json['amount']
                quantity = request.json['quantity']
                date = request.json['date']
            except:
                return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Data/Parameters'}),404)
            else:
                user = User.query.filter_by(id=id).all()
                if len(user) == 0:
                    return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'}),404)
                else:
                    user = user[0]
                    product = Products(request.json)
                    product.userID = id
                    db.session.add(product)
                    db.session.commit()
                    return jsonify({'data': product, 'message': 'Your report has been submitted sucessfully', 'error': ''})

@app.route('/getProducts', methods=['GET'])
def getProducts():
    try:
        token = request.headers['token']
    except:
        return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
    else:
        try:
            id = User.verifyToken(token=token)
        except:
            return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
        else:
            user = User.query.filter_by(id=id).all()
            if len(user) == 0:
                return  make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'}),404)
            else:
                user = user[0]
                allProducts = Products.query.filter_by(userID=id).all()
                return jsonify({'data': allProducts, 'message': 'Sucessfull', 'error': ''})

@app.route('/editProduct', methods=['POST'])
def editProduct():
    try:
        token = request.headers['token']
    except:
        return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
    else:
        try:
            id = User.verifyToken(token=token)
        except:
            return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
        else:
            try:
                # uid = request.json['uid']
                pid = request.json['pid']
                name = request.json['name']
                manufacture = request.json['manufacture']
                description = request.json['description']
                amount = request.json['amount']
                quantity = request.json['quantity']
                date = request.json['date']

            except:
                return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Data/Parameters'}),404)
            else:
                user = User.query.filter_by(id = id).all()
                if len(user) != 0:
                    user = user[0]
                    product = Products.query.filter_by(id=pid,userID=id).all()
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
                        return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid product id'}),404)
                else:
                    return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'}),404)


@app.route('/deleteProduct', methods=['DELETE'])
def deleteProduct():
    try:
        token = request.headers['token']
    except:
        return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
    else:
        try:
            id = User.verifyToken(token=token)
        except:
            return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
        else:
            try:
                pid = request.json['pid']
            except:
                return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Data/Parameters'}),404)
            else:
                user = User.query.filter_by(id = id).all()
                if len(user) != 0:
                    user = user[0]
                    product = Products.query.filter_by(id=pid,userID=id).all()
                    if len(product) != 0 :
                        product = product[0]
                        db.session.delete(product)
                        db.session.commit();
                        return jsonify({'data': '', 'message': 'Sucessfully Deleted', 'error': ''})
                    else:
                        return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Product with pid = ' + str(pid) + ' not available'}),404)
                else:
                    return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'User is not available with id  = ' + uid}),404)

@app.route('/addStores', methods=['POST'])
def addStores():
    try:
        token = request.headers['token']
    except:
        return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
    else:
        try:
            id = User.verifyToken(token=token)
        except:
            return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
        else:
            try:
                storeName = request.json['storeName']
                location = request.json['location']

            except:
                return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid Data/Parameters'}),404)
            else:
                user = User.query.filter_by(id=id).all()
                if len(user) != 0:
                    store = Store(request.json)
                    store.userID = id
                    db.session.add(store)
                    db.session.commit()
                    return jsonify({'data': store, 'message': 'Sucessfully Registered', 'error': ''})
                return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'User with ' + id + ' not registered'}),404)

@app.route('/getStores', methods=['GET'])
def getStores():
    try:
        token = request.headers['token']
    except:
        return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
    else:
        try:
            id = User.verifyToken(token=token)
        except:
            return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid token'}), 404)
        else:
            user = User.query.filter_by(id=id).all()
            if len(user) == 0:
                return make_response(jsonify({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'}),404)
            else:
                user = user[0]
                stores = Store.query.filter_by(userID=id).all()
                return jsonify({'data': stores, 'message': 'Sucessfull', 'error': ''}, )




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


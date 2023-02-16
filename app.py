from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api,Checkout


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)



#id
#title
#price
#isActive
class Item(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    isActive=db.Column(db.Boolean,default=True)
 #   text=db.Column(db.Text, nullable=False)
    def __repr__(self):
        return '<Article %r>'% self.id

with app.app_context():
    db.create_all()

@app.route('/home')
@app.route('/')
def index():
    items = Item.query.order_by(Item.id.desc()).all()
    return render_template('index.html',items=items)

@app.route('/buy/<int:id>')            # FONDY оплата
def buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,     #id компании
              secret_key='test')       #key компании
    checkout = Checkout(api=api)
    data = {
        "currency": "BYN",
        "amount": str(item.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create',methods=['POST','GET'])
def create():
    if request.method=='POST':
        title=request.form['title']
        price=request.form['price']#name

        item=Item(title=title,price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ошибочки у вас'
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)

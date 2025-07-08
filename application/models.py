from .database import db #since both the file is in the same directory, we can use'.database' to import it db object

#if we use application.database , it will search another directory named application
# and will not find the file, hence it will throw an error

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(400), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(10), nullable=False, default="general")  # 'user' or 'admin'

class Lots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(400), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    details = db.relationship('Spots', backref='lot', cascade="all, delete-orphan")


class Spots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'), nullable=False)
    status = db.Column(db.Boolean, default=False)   

class Reserve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('spots.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'cancelled'
    cost = db.Column(db.Float, nullable=False)
from flask import Flask,request,render_template,redirect

from flask import current_app as app #it refer to app object created

from .models import * #both is in same folder 
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")


@app.route('/')
@app.route('/login', methods= ['GET', 'POST'])        
def Login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        this_user = Users.query.filter_by(email=email).first() #get the first user with this email 
        if this_user:
            if this_user.password == password:
                if this_user.type == 'admin':
                    return redirect('/admin_dashboard')
                else:
                    return redirect(f'/user_dashboard/{this_user.id}')
            else:
                result = "Invalid password"
                return render_template("invalid_login.html", result=result)
        else:
            result = "User not found"
            return render_template("invalid_login.html", result=result)    
    return render_template('login.html') 


@app.route('/register', methods= ['GET', 'POST'])
def Register():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        fullname= request.form.get('fullname')
        address = request.form.get('address')
        pincode= request.form.get('pincode')
        this_user = Users.query.filter_by(email=email).first()
        if this_user:
            return 'User already exists'
        else:
            new_user = Users(email=email, password=password, fullname=fullname,address=address,pincode = pincode )
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
    return render_template('register.html')

@app.route('/user_dashboard/<user_id>', methods=['GET','POST'])
def user_dashboard(user_id):
    this_user = Users.query.filter_by(id=user_id).first()
    reserve = Reserve.query.filter_by(user_id=user_id).order_by(Reserve.start_time.desc()).limit(3).all()
    search = request.form.get('search') if request.method == 'POST' else None
    if search:
        this_lot = Lots.query.filter(Lots.location.contains(search)).all()
    else:
        this_lot = Lots.query.all()
    
    avail_spot = []
    for lot in this_lot:
        spot = Spots.query.filter_by(lot_id=lot.id, status="Available").first()
        if spot:
            avail_spot.append({'lot': lot, 'spot': spot.id})

    return render_template('user_dash.html', this_user=this_user, this_lot=this_lot, avail_spot=avail_spot, reserve=reserve)

@app.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    this_user = Users.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        this_user.email = request.form.get('email')
        this_user.password = request.form.get('password')
        this_user.fullname = request.form.get('fullname')
        this_user.address = request.form.get('address')
        this_user.pincode = request.form.get('pincode')
        db.session.commit()
        return redirect(f'/user_dashboard/{user_id}')
    return render_template('edit_user_prof.html', this_user=this_user)

@app.route('/book_spot/<int:user_id>/<int:lot_id>/<spot_id>', methods=['GET', 'POST'])
def book_spot(user_id, lot_id, spot_id):
    this_lot = Lots.query.filter_by(id=lot_id).first()
    if request.method == 'POST':
        start_time = datetime.now()
        vehicle_no = request.form.get('vehi_no') 
        status = "occupied"
        location = request.form.get('location')
        new_reservation = Reserve(user_id=user_id, lot_id=lot_id, location=location, spot_id=spot_id, start_time=start_time, vehicle_no=vehicle_no, status=status)
        db.session.add(new_reservation)
        db.session.commit()
        spot_to_update = Spots.query.filter_by(id=spot_id).first()
        spot_to_update.status = "Occupied"
        db.session.commit()
        this_lot.available_spots -= 1
        db.session.commit()
        return redirect(f'/user_dashboard/{user_id}')
    return render_template('Booking.html', user_id=user_id, lot_id=lot_id, spot_id=spot_id, this_lot=this_lot)


@app.route('/release/<int:user_id>/<int:lot_id>/<spot_id>', methods=['GET','POST'])
def release_spot(user_id, lot_id, spot_id):
    this_lot = Lots.query.filter_by(id=lot_id).first() 
    reserve1 = Reserve.query.filter_by(user_id=user_id, lot_id=lot_id, spot_id=spot_id, status="occupied").first()
    if request.method == 'POST':
        reserve1.status = "released" # released or occupied
        reserve1.end_time = datetime.now()
        reserve1.total_time = (reserve1.end_time - reserve1.start_time).total_seconds()/3600  # in hours
        reserve1.cost = (reserve1.end_time - reserve1.start_time).total_seconds() / 3600 * this_lot.price
        db.session.commit()
        spot_to_update = Spots.query.filter_by(id=spot_id).first()
        spot_to_update.status = "Available"  #   Available and Occupied
        db.session.commit()     
        this_lot.available_spots += 1
        db.session.commit()
        return redirect(f'/user_dashboard/{user_id}')
    return render_template('release.html', reserve1=reserve1, this_lot=this_lot, user_id=user_id)


@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    this_user = Users.query.filter_by(type="admin").first()
    all_users = Users.query.filter_by(type="user").all()
    all_lots = Lots.query.all()
    all_spots = Spots.query.all()
    all_reservations = Reserve.query.all()
    
    return render_template('admin_dash.html', all_users=all_users, all_lots=all_lots, all_spots=all_spots, all_reservations=all_reservations, this_user=this_user)

@app.route('/user_details', methods=['GET'])  
def user_details():
    all_users = Users.query.filter_by(type="user").all()
    this_user = Users.query.filter_by(type="admin").first()
    return render_template('admin_user.html', all_users=all_users,this_user=this_user)

@app.route('/edit_parking_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_parking_lot(lot_id):
    this_lot = Lots.query.filter_by(id=lot_id).first()
    if request.method == 'POST':
        this_lot.location = request.form.get('location')
        this_lot.price = request.form.get('price')
        this_lot.total_spots = request.form.get('max_spot')
        this_lot.available_spots = request.form.get('max_spot')
        this_lot.address = request.form.get('address')
        this_lot.pincode = request.form.get('pincode')
        db.session.commit()
        # Resetting the spots for the lot
        Spots.query.filter_by(lot_id=this_lot.id).delete()  # Delete existing spots
        db.session.commit()
        for i in range(1,int(this_lot.total_spots) + 1):
            spot_id = f"{this_lot.id}_{i}"
            update_spot = Spots(id=spot_id, lot_id=this_lot.id, status="Available")
            db.session.add(update_spot)
            db.session.commit()
        return redirect('/admin_dashboard')
    return render_template('edit_lot.html', this_lot=this_lot)

@app.route('/add_parking_lot', methods=['GET', 'POST'])
def add_parking_lot():
    if request.method == 'POST':
        location = request.form.get('location')
        price = request.form.get('price')
        max_spots = request.form.get('max_spot') # max_spots is the total number of spots
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        new_lot = Lots(location=location, price=price, total_spots=max_spots, available_spots=max_spots, address=address, pincode=pincode) 
        db.session.add(new_lot)
        db.session.commit()
        this_lot = Lots.query.filter_by(location=location).first()
        for i in range(1,int(max_spots) + 1):
            spot_id = f"{this_lot.id}_{i}"
            new_spot = Spots(id=spot_id, lot_id=new_lot.id, status="Available")
            db.session.add(new_spot)
            db.session.commit()
        return redirect('/admin_dashboard')
    return render_template('add_lot.html')

@app.route('/delete_spot/<spot_id>', methods=['GET', 'POST'])
def delete_spot(spot_id):
    this_spot = Spots.query.filter_by(id=spot_id).first()
    if request.method == 'POST':
        db.session.delete(this_spot)
        db.session.commit()
        lot_id = this_spot.lot_id
        this_lot = Lots.query.filter_by(id=lot_id).first()
        this_lot.available_spots -= 1
        this_lot.total_spots -= 1
        db.session.commit()
        return redirect('/admin_dashboard')
    return render_template('delete_spot.html', this_spot=this_spot)

@app.route('/delete_lot/<int:lot_id>', methods=['GET', 'POST'])
def delete_lot(lot_id):
    this_lot = Lots.query.filter_by(id=lot_id).first()
    if this_lot:
        db.session.delete(this_lot)
        db.session.commit()
    return redirect('/admin_dashboard')


@app.route('/occupied_spot_detail/<spot_id>', methods=['GET'])
def occupied_spot_detail(spot_id):
    this_spot_reserve = Reserve.query.filter_by(spot_id=spot_id, status="occupied").first()
    return render_template('parking_spot_details.html', this_spot_reserve=this_spot_reserve) 

@app.route('/search')
def search():
    this_user = Users.query.filter_by(type="admin").first()
    search = request.args.get('search')
    key = request.args.get('key')
    if key == "user":
        results = Users.query.filter(Users.fullname.contains(search)).first()
        if results:
            user_reserve = Reserve.query.filter_by(user_id=results.id).order_by(Reserve.id.desc()).all()
        else:
            user_reserve = None     
    else:
        results = Lots.query.filter(Lots.location.contains(search)).all()
    all_spots = Spots.query.all()
    return render_template('search.html', results=results, this_user=this_user, key=key, all_spots=all_spots, user_reserve=user_reserve if key == "user" else None)

@app.route('/admin_summary', methods=['GET'])
def admin_summary():
    this_user = Users.query.filter_by(type="admin").first()
    total_user = len(Users.query.filter_by(type="user").all())
    total_lots = len(Lots.query.all())
    all_lots = Lots.query.all()
    all_spots = Spots.query.all()
    total_spot = len(all_spots)
    total_available_spots = len([spot for spot in all_spots if spot.status == "Available"])

    labels = [lot.location for lot in all_lots]
    sizes = [len(Spots.query.filter_by(lot_id=lot.id).all()) for lot in all_lots]
    plt.bar(labels,sizes)
    plt.xlabel("Lot Location")
    plt.ylabel("No of Spots")
    plt.title("No. Spots in Each Lot")
    plt.savefig("static/bar.png")
    plt.clf()

    return render_template('summ_admin.html', this_user=this_user, total_user=total_user, total_lots=total_lots, 
                           total_spot=total_spot, total_available_spots=total_available_spots)

@app.route('/user_summary/<int:user_id>', methods=['GET'])
def user_summary(user_id):
    this_user = Users.query.get(user_id)
    reserve = Reserve.query.filter_by(user_id=user_id, status="released").order_by(Reserve.id.desc()).all()
    return render_template('summ_user.html', this_user=this_user, reserve=reserve)

@app.route('/all_reservations', methods=['GET'])
def all_reservations():
    this_user = Users.query.filter_by(type="admin").first()
    all_reserve = Reserve.query.filter_by(status = "released").order_by(Reserve.id.desc()).all()
   
    return render_template('all_reserve.html', this_user=this_user, all_reserve=all_reserve)
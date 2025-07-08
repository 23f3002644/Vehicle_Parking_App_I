from flask import Flask,request,render_template,redirect,request

from flask import current_app as app #it refer toapp object created

from .models import * #both is in same folder 

@app.route('/login', methods= ['GET', 'POST'])
def Login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        this_user = Users.query.filter_by(email=email).first() #get the first user with this email

        if this_user:
            if this_user.password == password:
                if this_user.type == 'admin':
                    return render_template('admin_dash.html', user=this_user.fullname)
                else:
                    return render_template('user_dash.html', user=this_user.fullname)
            else:
                return 'Invalid password'
        else:
            return 'User not found'    
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
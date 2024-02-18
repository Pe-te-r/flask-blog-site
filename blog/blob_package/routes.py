from flask import  render_template, request, redirect, url_for,flash,abort
from flask_login import current_user,logout_user,login_user,login_required
from blob_package.forms import Registration,Login,UpdateAccount,PostForm
from uuid import uuid4
from blob_package import app,db,bcrypt
from blob_package.models import User,Post


@app.route('/')
@login_required
def index():
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('index.html',posts=posts)

@app.route('/register',methods=['POST','GET'])
def register():
    form=Registration()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method=='POST' and form.validate_on_submit():
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')

        same_user=User.query.filter_by(username=username).first()
        same_email=User.query.filter_by(email=email).first()

        if same_user:
           flash('the username already exists','warning')
        elif same_email:
            flash('the email already exists','warning')
        else:
            hashed=bcrypt.generate_password_hash(password).decode('utf-8')
            user=User(id=uuid4(),username=username,email=email,password=hashed)
            db.session.add(user)
            db.session.commit()

            login_user(user,remember=True)

            flash(f'account created for {form.username.data}!','success')

            return redirect(url_for('index'))
    
    return render_template('register.html',form=form)
    

@app.route('/login',methods=['POST','GET'])
def login():
    form=Login()
    if request.method=='POST' and form.validate_on_submit():
        email=request.form.get('email')
        password=request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password,password):
            flash('logged in successfully','success')
            next_page=request.args.get('next')
            login_user(user,remember=True)
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('login unsuccessfully, check your email or password','danger')
            print('wrong details')
    return render_template('login.html',form=form)


@app.route('/forgot_password')
def forgot_password():
    return 'To be available soon be patient'


@app.route('/profile',methods=['POST','GET'])
@login_required
def profile():
    form=UpdateAccount()
    if request.method=='POST' and form.validate_on_submit():
    # if form.validate_on_submit():
        if form.username.data == current_user.username:

            email=request.form.get('email')
            mail_duplicate=User.query.filter_by(email=email).first()

            if mail_duplicate :
                flash('the email already exists','warning')
            else:

                current_user.email=form.email.data
                db.session.commit()
                flash('your account email have been updated','success')
        elif form.email.data == current_user.email:
            username=form.username.data
            username_duplicate=User.query.filter_by(username=username).first()

            if username_duplicate:
                flash('the username already exists','warning')
            else:
                current_user.username=form.username.data
                db.session.commit()
                flash('your account username have been updated','success')
        else:
            current_user.username=form.username.data
            current_user.email=form.email.data
            db.session.commit()
            flash('your account have been updated','success')
        
        return redirect(url_for('profile'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
        db.session.commit()

    return render_template('profile.html',form=form)

@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))           


@app.route('/post/new',methods=['POST','GET'])
@login_required
def new_post():
    try:

        form=PostForm()
        if form.validate_on_submit():
            post=Post(title=form.title.data,content=form.content.data,author=current_user)
            with app.app_context():
                db.create_all()
                db.session.add(post)
                db.session.commit()
            flash('You post have been created','success')
            return redirect(url_for('index'))
        return render_template('new_post.html',form=form)
    except Exception as e:
        db.session.rollback()
        return None

@app.route('/post/<uuid:post_id>')
def post(post_id):
    post=Post.query.get_or_404(post_id)

    return render_template('post.html',post=post)

@app.route('/post/<uuid:post_id>/update',methods=['GET','POST'])
@login_required
def post_update(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    form=PostForm()

    if form.validate_on_submit() and request.method=='POST':
        
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('post have been updated','success')

        
        return redirect(url_for('post',post_id=post.id))
    
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
        form.submit.label.text="update"

    return render_template('update.html',form=form,post=post)

@app.route('/delete/<uuid:item_id>')
def delete(item_id):
    post=Post.query.get(item_id)

    if post:
        try:
            db.session.delete(post)
            db.session.commit()
            flash('your post deleted succesfully','success')
        except:
            db.session.rollback()
    
    return redirect(url_for('index'))

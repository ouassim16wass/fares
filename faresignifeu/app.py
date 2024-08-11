from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import pyodbc

app = Flask(__name__)
app.secret_key = 'Alger'  # Définir la clé secrète


def connect_to_database():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=HP\\SQLEXPRESS;DATABASE=a2mouche;Trusted_Connection=yes;')
    return conn

# Configuration pour Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ouassimmegrad0@gmail.com'
app.config['MAIL_PASSWORD'] = 'tchj izbg eljw lfyy'  # Consider using environment variables for security
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/order_form', methods=['GET', 'POST'])
def order_form():
    service = request.args.get('service')
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
       
        service_type = request.form['service_type']
        message = request.form['message']
        address = request.form['address']

        # Construct the email message
        msg = Message(
            subject='Nouvelle Commande',
            sender='ouassimmegrad0@gmail.com',  # Ensure the sender matches your mail username
            recipients=['wassimmegrad1@gmail.com']
        )
        
        # Format the message body
        msg.body = (
            f"Nom: {name}\n"
            f"Email: {email}\n"
            f"Téléphone: {phone}\n"
          
            f"Type de service: {service_type}\n"
            f"Message: {message}\n"
            f"Adresse: {address}"
        )

        try:
            # Send the email
            mail.send(msg)
            flash('Votre commande a été envoyée avec succès ! Vous allez recevoir un appel prochainement pour fixer une date et discuter du prix.')
            return redirect(url_for('order_confirmation'))
        except Exception as e:
            # Log the exception or handle it appropriately
            flash('Une erreur est survenue lors de l\'envoi de votre commande. Veuillez réessayer plus tard.')
            print(f"Erreur d'envoi de l'email: {e}")

    return render_template('order_form.html', service=service)



@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about_us')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

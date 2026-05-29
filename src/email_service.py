import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def sendMail(destinatario, nombre, area, fecha, hora):

    try:

        remitente = os.getenv('MAIL_FROM')
        mensaje = MIMEText(f"""
Hola {nombre}

Tu cita en Bella Piel ha sido agendada y confirmada.

Área: {area}

Fecha: {fecha}

Hora: {hora}

¡Te esperamos!
Recuerda que solamente tenemos 5 minutos de tolerancia.
Lindo día.
""")

        mensaje['Subject'] = 'Confirmación de cita Bella Piel'
        mensaje['From'] = remitente
        mensaje['To'] = destinatario

        servidor = smtplib.SMTP(
            os.getenv('MAIL_SERVER'),
            int(os.getenv('MAIL_PORT'))
        )

        servidor.starttls()

        servidor.login(
            os.getenv('MAIL_USERNAME'),
            os.getenv('MAIL_PASSWORD')
        )

        servidor.send_message(mensaje)

        servidor.quit()

        print("Correo enviado correctamente")

        return True

    except Exception as e:

        print("ERROR CORREO:", e)

        return False

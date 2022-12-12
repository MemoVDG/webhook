import os
import sys

from os.path import dirname, join, abspath
from flask import Flask, request, abort

from managers.email_manager import EmailManager

sys.path.insert(0, abspath(join(dirname(__file__), '.')))

app = Flask(__name__)
app.secret_key = "SECRET_KEY"


@app.route('/', methods=['GET'])
def index():
    return "Success", 200, {"Access-Control-Allow-Origin": "*"}


# TODO: Validate sign to avoid requests from any source
@app.route('/webhook', methods=['POST', ])
def webhook():
    if request.method == 'POST':
        data = request.get_json()
        email_manager = EmailManager(
            sender='memovdg@gmail.com',
            password=os.environ['GMAIL_PASSWORD'],
        )
        # TODO: Move validation in decorator
        expected_keys = {
            'user_name',
            'date',
            'user_email',
        }
        if expected_keys <= data.keys():
            message = f"Hi, you got a new reservation for {data['date']}, please contact with {data['user_name']} to confirm the tour"
            if os.environ['ENV'] == 'PRODUCTION':
                email_manager.send_email(
                    message=message,
                    receivers=data['user_email'],
                )
            return "Success", 200, {"Access-Control-Allow-Origin": "*"}
        else:
            abort(400)
    else:
        abort(400)


if __name__ == '__main__':
    app.run()

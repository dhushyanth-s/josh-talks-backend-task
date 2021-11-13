from flask import Flask
from threading import Thread
from background import background

app = Flask(__name__)

Thread(target=background).start()
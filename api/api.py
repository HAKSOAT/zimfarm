from flask import Flask
from celery import Celery

from .template import template


def configure() -> (Flask):
    flask = Flask(__name__)
    flask.config['CELERY_BROKER_URL'] = 'pyamqp://celery:celery@localhost/celeryvhost'
    flask.config['CELERY_RESULT_BACKEND'] = 'rpc://'

    # celery = Celery(flask.name, broker=flask.config['CELERY_BROKER_URL'],
    #                 backend=flask.config['CELERY_RESULT_BACKEND'])
    # celery.conf.update(flask.config)

    return flask

app = configure()
app.route('/template', methods=['GET'])(template)


if __name__ == "__main__":
    app.run()
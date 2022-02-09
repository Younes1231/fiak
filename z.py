# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
from flaski.models import WikiContent
from flaski.database import db_session
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
def hello():
    contents = WikiContent.query.all()
    return render_template("index.html", contents=contents)


@app.route("/<title>", methods=["GET"])
def show_content(title):
    content = WikiContent.query.filter_by(title=title).first()
    if content is None:
        abort(404)
    return render_template("show_content.html", content=content)

@app.route("/<title>", methods=["POST"])
def post_content(title=None):
    if title is None:
        abort(404)
    content = WikiContent.query.filter_by(title=title).first()
    #Si le contenu ne peut pas être obtenu, insérez-le, créez donc une instance de WikiContent.
    if content is None:
        content = WikiContent(title,
                              request.form["body"]
                              )
    #Si le contenu peut être obtenu, il sera mis à jour, donc le contenu du corps et datetime=Réglez l'heure actuelle
    else:
        content.body = request.form["body"]
        content.date = datetime.now()

    #Ajouter le contenu du contenu et s'engager
    db_session.add(content)
    db_session.commit()
    return content.body

if __name__ == "__main__":
    app.run()
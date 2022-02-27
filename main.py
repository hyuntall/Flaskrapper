from flask import Flask, render_template, request, redirect, send_file
from jobScrap import getJobs
from exporter import save_to_file

app = Flask("UserScrapper")

db = {}


@app.route("/")
def home():
    return render_template("hi.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = getJobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("report.html",
                           searchingBy=word,
                           resultsNumber=len(jobs),
                           jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        save_to_file(jobs)
        if not jobs:
            raise Exception()
        return f"Generate CSV for {word}"
    except:
        return redirect("/")


if __name__ == '__main__':
    app.run(host="0.0.0.0")

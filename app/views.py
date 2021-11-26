from app import app
from flask import render_template, jsonify

import os
import psycopg2


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/db")
def db():
    conn = psycopg2.connect(
        os.environ.get("DATABASE_URL", "postgres://postgres:postgres@db:5432/postgres")
    )

    cur = conn.cursor()

    with conn.cursor as cur:
        cur.execute(
            """
            SELECT
                *
            FROM
                cumulative
            """
        )

        row_headers = [x[0] for x in cur.description]  # this will extract row headers
        rv = cur.fetchall()

    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    return jsonify(json_data)


@app.route("/db/koic")
def db_koi_disposition_confirmed():
    conn = psycopg2.connect(
        os.environ.get("DATABASE_URL", "postgres://postgres:postgres@db:5432/postgres")
    )

    cur = conn.cursor()

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                *
            FROM
                cumulative
            WHERE
                koi_disposition = 'CONFIRMED'
            """
        )

        row_headers = [x[0] for x in cur.description]  # this will extract row headers
        rv = cur.fetchall()

    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    return jsonify(json_data)


@app.route("/db/<int:kepid>")
def db_kepid(kepid):
    conn = psycopg2.connect(
        os.environ.get("DATABASE_URL", "postgres://postgres:postgres@db:5432/postgres")
    )

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                *
            FROM
                cumulative
            WHERE
                kepid = %(kepid)s
            """,
            {"kepid": kepid},
        )

        row_headers = [x[0] for x in cur.description]  # this will extract row headers
        rv = cur.fetchall()

    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    return jsonify(json_data)

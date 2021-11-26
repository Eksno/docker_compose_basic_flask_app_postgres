from app import app
from flask import render_template, jsonify

import os
import logging
import psycopg2


@app.route("/")
@app.route("/home")
def home():
    logging.info("/ or /home loaded")
    return render_template("home.html")


@app.route("/db")
def db():
    logging.info("/db loaded")
    conn = psycopg2.connect(
        os.environ.get("DATABASE_URL", "postgres://postgres:postgres@db:5432/postgres")
    )
    logging.debug("connected to database")

    with conn.cursor() as cur:
        logging.debug("opened cursor")
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
    logging.debug("exited cursor")

    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    logging.debug("created json data")

    return jsonify(json_data)


@app.route("/db/koic")
def db_koi_disposition_confirmed():
    logging.info("/db/koic loaded")
    conn = psycopg2.connect(
        os.environ.get("DATABASE_URL", "postgres://postgres:postgres@db:5432/postgres")
    )
    logging.debug("connected to database")

    with conn.cursor() as cur:
        logging.debug("opened cursor")
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
    logging.debug("exited cursor")

    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    logging.debug("created json data")

    return jsonify(json_data)


@app.route("/db/<int:kepid>")
def db_kepid(kepid):
    logging.info(f"/db/{kepid} loaded")
    conn = psycopg2.connect(
        os.environ.get("DATABASE_URL", "postgres://postgres:postgres@db:5432/postgres")
    )
    logging.debug("connected to database")

    with conn.cursor() as cur:
        logging.debug("opened cursor")
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
    logging.debug("exited cursor")

    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    logging.debug("created json data")

    return jsonify(json_data)

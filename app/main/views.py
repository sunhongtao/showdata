from . import main
from flask import render_template, Response, json
import pymysql


@main.route('/', methods=['GET', 'POST'])
def index():
    sql_info = "SELECT DISTINCT LEVEL from icinga_info"
    result = get_warning_level(sql_info)
    return render_template('index.html', result=result)


def get_warning_level(sql_info):
    db = pymysql.connect(host="localhost", user="root",
                         password="root", db="alert_info", port=3306)
    cur = db.cursor()
    try:
        cur.execute(sql_info)
        result = cur.fetchall()
    except Exception as e:
        raise e
    finally:
        db.close()
    return result


@main.route('/ajax/getIP', methods=['GET'])
def get_ip(request):
    level = request.args.get('level')
    sql_info = 'SELECT DISTINCT ip from icinga_info WHERE LEVEL = {}'.format(level)
    ip = get_warning_level(sql_info)
    print(ip)
    result = {}
    result["ip"] = ip
    return Response(json.dumps(), content_type='application/json')

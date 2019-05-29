import time

from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.views.decorators.http import condition
import urllib.parse as urlparse

from cn.api_models import *
from cnWeb.urls import a
from cnWeb.urls import mysqlPool

from django.http import JsonResponse

# Create your views here.
from cnWeb.urls import mysqlPool
from notification_sender import notify
from . import api_models
import json
print("in view one")
@csrf_exempt
def enterDatatodb(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    cur = a.cursor()
    cur.execute("INSERT INTO user (uid, name, email,fcm_id)SELECT * FROM (SELECT '{}', '{}', '{}','{}') AS tmp WHERE NOT EXISTS (SELECT uid FROM user WHERE uid = '{}') LIMIT 1;"

                .format(body[User.uid],body[User.name],body[User.email],body[User.fcm_id],body[User.uid]))

    cur.close()
    a.commit()
    
    # content = body['content']

    return JsonResponse({'success':"data_entered_successfully"})

@csrf_exempt
def enterlocationdata(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    formatted_date = datetime.strptime(body['date'].split('.')[0],'%Y-%m-%dT%H:%M:%S')
    notifyParent( body[LocationData.uid])
    conn=mysqlPool.get_connection()
    cur=conn.cursor()


    cur.execute("INSERT into location_data( lat, place, lon, uid, day, time, month, datetime, parent_uid)values ('{}' , '{}','{}','{}','{}','{}','{}','{}','{}' );"

                .format(
        body[LocationData.lat],

        body[LocationData.place],
        body[LocationData.lon],
        body[LocationData.uid],
        body[LocationData.day],
        body[LocationData.time],
        body[LocationData.month],
        formatted_date,
        'kkjol'
                        ))



    cur.close()
    conn.commit()
    conn.close()
    print(body)
    return JsonResponse({'success':"data_entered_successfully"})

@csrf_exempt
def addParent(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    conn = mysqlPool.get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_parent (puid, uid) SELECT * FROM (SELECT '{}','{}') AS tmp WHERE NOT EXISTS (SELECT puid ,uid FROM user_parent WHERE puid='{}' and uid = '{}') LIMIT 1;"

                .format(body['parent'],body['child'],body['parent'],body['child'])
                )

    cur.close()
    conn.commit()
    conn.close()
    print(body)
    return JsonResponse({'success': "data_entered_successfully"})

# @condition(etag_func=None)
def getUsers(request):
# return StreamingHttpResponse( stream_response_generator(), content_type='application/json')
#     body_unicode = request.body.decode('utf-8')
#     body = json.loads(body_unicode)
    conn = mysqlPool.get_connection()
    cur = conn.cursor()

    list=[]



    cur.execute("Select * from user")

    for row in cur:
        list.append(row)

    cur.close()
    conn.commit()
    conn.close()
    # print(body)
    return JsonResponse({"success": list})

# def stream_response_generator():
#     for x in range(1,6):
#         yield {'a':1}
#         time.sleep(1)


@csrf_exempt
def getuserdetails(request):

    print(request.GET.get('uid'))

    conn = mysqlPool.get_connection()
    cur = conn.cursor()
    list1 = []

    cur.execute("select * from location_data where uid='{}' order by datetime desc ;".format(request.GET.get('uid')))
    for row in cur:
        list1.append(row)

    cur.close()
    conn.commit()
    conn.close()
    return JsonResponse({'success': list1})


def updateFcm(request):
    uid=request.GET.get('uid')
    fcm=request.GET.get('fcm')
    conn = mysqlPool.get_connection()
    cur = conn.cursor()
    cur.execute("update user set fcm_id= '{}' where uid='{}'".format(fcm,uid))

    cur.close()
    conn.commit()
    conn.close()

    return JsonResponse({"success": 'suop'})

def notifyParent(uid):

    conn = mysqlPool.get_connection()
    cur = conn.cursor()


    cur.execute("select puid from user_parent where uid='{}'".format(uid))

    for i in cur:
        conn1 = mysqlPool.get_connection()
        cur1 = conn.cursor()

        cur1.execute("select fcm_id from user where uid='{}';".format(i[0]))

        for j in cur1:
            notify(j[0], "ur child ", "check his location")


        cur1.close()
        conn1.commit()
        conn1.close()




    cur.close()
    conn.commit()
    conn.close()
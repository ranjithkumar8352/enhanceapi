import cv2
import os
import datetime
from flask import json
import numpy as np
import requests
from skimage.filters import threshold_adaptive
from flask import make_response
from flask import request


def imgweb():
    if request.method == 'GET':
        return """<html>
                    <head>
                    <style type="text/css">.thumb-image{float:left;width:100px;position:relative;padding:5px;}</style>
                    </head>
                    <body>
                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
                    <form enctype="multipart/form-data" method="POST">

                    <input type="file" id="fileUpload" name="file" multiple>
                    <input type="text" name="profileId">
                    <input type="text" name="courseId">
                    <input type="submit" value="Submit">
                    </form>
                    <div id="image-holder"></div>

                    </div>

                    <script>
                    $(document).ready(function() {
                            $("#fileUpload").on('change', function() {
                              //Get count of selected files
                              var countFiles = $(this)[0].files.length;
                              var imgPath = $(this)[0].value;
                              var extn = imgPath.substring(imgPath.lastIndexOf('.') + 1).toLowerCase();
                              var image_holder = $("#image-holder");
                              image_holder.empty();
                              if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {
                                if (typeof(FileReader) != "undefined") {
                                  //loop for each file selected for uploaded.
                                  for (var i = 0; i < countFiles; i++)
                                  {
                                    var reader = new FileReader();
                                    reader.onload = function(e) {
                                      $("<img />", {
                                        "src": e.target.result,
                                        "class": "thumb-image"
                                      }).appendTo(image_holder);
                                    }
                                    image_holder.show();
                                    reader.readAsDataURL($(this)[0].files[i]);
                                  }
                                } else {
                                  alert("This browser does not support FileReader.");
                                }
                              } else {
                                alert("Pls select only images");
                              }
                            });
                          });
                    </script>
                    </body>
                    </html>"""
    else:
        try:
            fileList = request.files.getlist('file')
        except Exception, E:
            print "file Missing in request"
            obj = {'response': 1, 'description': "file Missing in request"}
            return json.dumps(obj)
        try:
            profileId = request.form['profileId']
        except Exception, E:
            profileId = "defaultProfile"
        try:
            courseId = request.form['courseId']
        except Exception, E:
            courseId = "defaultCourse"
        urlList = []
        for file in fileList:
            timestamp = "".join(str(datetime.datetime.now()).split())
            fileName = '/var/www/uploads/' + timestamp + '.jpg'
            file.save(fileName)
            img = cv2.imread(fileName, 0)
            #enhanced = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            enhanced = threshold_adaptive(img, 51, offset=10)
            enhanced = enhanced.astype("uint8") * 255
            cv2.imwrite(fileName, enhanced, [int(cv2.IMWRITE_JPEG_QUALITY), 20])
            data = {'profileId':profileId,'courseId':courseId }
            print json.dumps(data)
            apiUrl = "https://uploadnotes-2016.appspot.com/imgweb"
            files = {'file': open(fileName, 'rb')}
            r = requests.post(apiUrl,data=data, files=files)
            try:
                r = json.loads(r.text)
            except Exception, E:
                r = r.text
            print r
            try:
                imageUrl = r['url'][0]
            except Exception, E:
                imageUrl = ""
            urlList.append(imageUrl)
            os.remove(fileName);
        obj = {'response': 0, 'url': urlList}
        response = make_response(json.dumps(obj))
        response.headers['Content-Type'] = 'application/json'
        return response

def imgandroid():
    if request.method == 'GET':
        return """<form method="POST" enctype="multipart/form-data">
                                    <input type="file" name="file">
                                    <input type="submit" name="submit">
                                   </form>"""
    else:
        try:
            fileList = request.files.getlist('file')
        except Exception, E:
            print "file Missing in request"
            #obj = {'response': 1, 'description': "file Missing in request"}
            #response = make_response(json.dumps(obj))
            #response.headers['Content-Type'] = 'application/json'
            #return json.dumps(obj)
            fileList = ""
        try:
            profileId = request.form['profileId']
        except Exception, E:
            print "profileId missing in request"
            return "profileId missing in request"
        try:
            courseId = request.form['courseId']
        except Exception, E:
            print "courseId missing in request"
            return "courseId missing in request"
        try:
            title = request.form['title']
        except Exception, E:
            print "title Missing in request"
            return "title Missing in request"
        try:
            desc = request.form['desc']
        except Exception, E:
            print "desc Missing in request"
            return "desc Missing in request"
        try:
            type = request.form['type']
        except Exception, E:
            print "type Missing in request"
            return "type Missing in request"
        try:
            date = request.form['date']
        except Exception, E:
            date = ""
        try:
            dueDate = request.form['dueDate']
        except Exception, E:
            dueDate = ""
        try:
            dueTime = request.form['dueTime']
        except Exception, E:
            print "no dueTime"
            dueTime = "12:00"
        files = []
        if len(fileList) > 0:
            for file in fileList:
                timestamp = "".join(str(datetime.datetime.now()).split())
                fileName = timestamp + '.jpg'
                file.save(fileName)
                img = cv2.imread(fileName, 0)
                #enhanced = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                enhanced = threshold_adaptive(img, 51, offset=10)
                enhanced = enhanced.astype("uint8") * 255
                cv2.imwrite(fileName, enhanced)
                files.append(('file', open(fileName, 'rb')))
                os.remove(fileName);
        data = {'profileId':profileId,'courseId':courseId, 'title':title ,'desc':desc,'date':date, 'dueDate' :dueDate, 'dueTime':dueTime, 'type':type }
        print json.dumps(data)
        url = "https://uploadnotes-2016.appspot.com/img"
        r = requests.post(url,data=data, files=files)
        try:
            r = json.dumps(r.json())
        except Exception, E:
            r = r.text
        response = make_response(r)
        response.headers['Content-Type'] = 'application/json'
        print r
        return response
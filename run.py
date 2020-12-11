from flask import Flask, escape, request, jsonify, make_response, render_template
import json
import os
import time
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'secret!'

# 判斷是否為圖片
def isPhoto(imgpath):
    if(imgpath.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))):
        return True
    else:
        return False

@app.route('/showUser', methods=['GET'])
def showUser():
    userPhotoDic = dict()
    dirlist = os.listdir('photo')
    for dirname in dirlist:
        if os.path.isdir('photo/'+dirname):
            filelist = os.listdir('photo/'+dirname)
            for name in filelist:
                if isPhoto('photo/'+dirname+'/'+name):
                    if dirname not in userPhotoDic:
                        userPhotoDic[dirname] = list()
                    userPhotoDic[dirname].append(dirname+'/'+name)
    return render_template('showUser.html', data=userPhotoDic)



@app.route('/delfile/<string:mydir>/<string:filename>', methods=['GET'])
# 刪除圖片資料
def delfile(mydir, filename):
    if request.method == "GET":
        # if os.path.isdir(os.path.join(mydir+'/'+myid, '%s' % filename)):
        try:
            os.remove(os.path.join('photo/'+mydir+'/', '%s' % filename))
        except OSError as e:
            print(e)
            return "查無檔案"

        return render_template('close.html')


@app.route('/getUserPhoto/<string:mydir>/<string:filename>', methods=['GET'])
# 取得圖片
def getUserPhoto(mydir, filename):
    image_data = open(os.path.join(
        'photo/'+mydir+'/', '%s' % filename), "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route("/userPhoto", methods=['POST', "GET"])
def userPhoto():
    jsondata = json.loads(request.values['my_data'])
    jsondata['time'] = str(time.time())
    img = request.files.get('file')
    # 使用時間戳記當作檔案名稱
    fileName = str(time.time())
    # 檢查資料夾是否存在
    if not os.path.isdir("photo/"):
        os.mkdir("photo/")
    if not os.path.isdir("photo/"+jsondata['name']):
        os.mkdir("photo/"+jsondata['name'])
    filename = "photo/"+jsondata['name']+"/"+fileName+".png"
    img.save(filename)
    return jsonify(jsondata)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

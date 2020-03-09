from flask import Flask, render_template, request, url_for
import sys

import plotly
from plotly.graph_objs import Scatter, Layout
import json

import requests
from xml.etree import ElementTree


app = Flask(__name__)
URL="http://www.garak.co.kr/publicdata/dataOpen.do"

# @app.route("/")
# def hello():
#     # return render_template('first_page.html')
#     return "Hi, please go to /~~"

@app.route('/')
def main_get(num=None):
    return render_template('first_page.html', pum_nm=1)


@app.route('/first_page', methods=['POST', 'GET'])
def first_page(num=None):
    ## 어떤 http method를 이용해서 전달받았는지를 아는 것이 필요함
    ## 아래에서 보는 바와 같이 어떤 방식으로 넘어왔느냐에 따라서 읽어들이는 방식이 달라짐
    if request.method == 'POST':
        #temp = request.form['num']
        pass
    elif request.method == 'GET':
        ## 넘겨받은 숫자 
        p_ymd   = request.args.get('p_ymd')
        p_ymd   = int(p_ymd)
        p_jymd  = request.args.get('p_jymd') 
        p_jjymd = request.args.get('p_jjymd') 
        pum_nm = request.args.get('pum_nm') 
        # params = {'id': '2697',
        #   'passwd': 'Xptmxm100!!',
        #   'dataid': 'data4',
        #   'pagesize': '10',
        #   'pageidx': '1',
        #   'portal.templet' : 'false',
        #   'p_ymd': '20200213',
        #   'p_jymd': '20200212',
        #   'd_cd': '2',
        #   'p_jjymd': '20190213',
        #   'p_pos_gubun': '1',
        #   'pum_nm': '귤'}
        params = {'id': '2697',
          'passwd': 'Xptmxm100!!',
          'dataid': 'data4',
          'pagesize': '10',
          'pageidx': '1',
          'portal.templet' : 'false',
          'd_cd': '2',
          'p_pos_gubun': '1'}
        params.setdefault('pum_nm', pum_nm)
        params.setdefault('p_ymd', p_ymd)
        params.setdefault('p_jymd', p_jymd)
        params.setdefault('p_jjymd', p_jjymd)
        params.update(p_ymd = p_ymd)
        # params.update(p_jymd = p_jymd)
        # params.update(p_jjymd = p_jjymd)
        res = requests.get(URL, params=params)
        tree = ElementTree.fromstring(res.content)
        
        
        # for list_tag in tree.findall('./list'):
        #     grade_tag = list_tag.find('G_NAME_A')
        #     unit_tag = list_tag.find('U_NAME')
        #     if grade_tag.text == '상' and unit_tag.text == '  10키로상자':
        #         avr_price_tag = list_tag.find('AV_P_A')
        #         temp1 = grade_tag.text
        #         temp2 = avr_price_tag.text

        data_val = []
        data_num = []
        child_tags_val = None
        
        for i in range(0,100):
            for list_tag in tree.findall('./list'):     
                child_tags_gade = list_tag.find('G_NAME_A').text
                child_tags_unit = list_tag.find('UNIT_QTY').text
                if child_tags_gade == "상" and child_tags_unit == "   3" :
                    child_tags_val = list_tag.find('AV_P_A').text
                    child_tags_val_r = float(child_tags_val)
                    data_val = data_val + [child_tags_val_r]
                    data_num = data_num + [i]
            p_ymd2 = p_ymd + (i//30)*100+(i%30)
            params.update(p_ymd = p_ymd2)
            res = requests.get(URL, params=params)
            tree = ElementTree.fromstring(res.content)
        data = Scatter(x = data_num, y = data_val)
        graphJSON = json.dumps(data, cls = plotly.utils.PlotlyJSONEncoder)
        print(data_val)
        
                
    return render_template('dashboard_test.html', plot = graphJSON)
        
    #     data1 = ''
    #     for list_tag in tree.findall('./list'):
    #         child_tags = list_tag.findall('*')
    #         data = ''
    #         for child_tag in child_tags:
    #             data = data + '\t' + child_tag.text
    #         data1 = data1 + data + '<br>'
        
    # return data1

                
                
                
        # return render_template('first_page.html', data1 = temp1, data2 = temp2)

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(sys.argv[1]))

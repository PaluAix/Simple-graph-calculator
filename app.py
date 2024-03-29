from flask import Flask, request, jsonify, send_from_directory
import csv
from algorithms import find_shortest_path, find_longest_path
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

""" @app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        global graph
        graph = process_csv(file)
        return jsonify({'message': '文件上传成功，可以进行计算了。'})
    else:
        return jsonify({'message': '上传失败，请重试。'}) """
        
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        global graph
        graph, is_valid, error = process_csv(file)
        if not is_valid:
            return jsonify({'error': True, 'message': error}), 400  # 返回400状态码及错误信息
        return jsonify({'error': False, 'message': '文件上传成功，可以进行计算了。'})
    else:
        return jsonify({'error': True, 'message': '上传失败，请重试。'}), 400

# 这里加个误操作告警，防呆
@app.route('/shortest', methods=['GET'])
def shortest_path():
    start = request.args.get('start', 'A')
    end = request.args.get('end', 'B')
    if not graph:
        return jsonify({'error': '图数据为空，请先上传文件。'})
    result = find_shortest_path(graph, start, end)
    return jsonify({'result': result})

@app.route('/longest', methods=['GET'])
def longest_path():
    if not graph:
        return jsonify({'error': '图数据为空，请先上传文件。'})
    result = find_longest_path(graph)
    return jsonify({'result': result})

def process_csv(file):
    graph = {}
    reader = csv.reader(file.read().decode('utf-8').splitlines(), delimiter=' ')
    for row in reader:
        if len(row) != 3:
            return {}, False, "文件格式不正确，每行应该包含三个由空格分隔的值。"
        s, t, v = row
        if s not in graph:
            graph[s] = {}
        graph[s][t] = int(v)
    return graph, True, ""

""" def process_csv(file):
    graph = {}
    reader = csv.reader(file.read().decode('utf-8').splitlines(), delimiter=' ')
    for row in reader:
        s, t, v = row
        if s not in graph:
            graph[s] = {}
        graph[s][t] = int(v)
    return graph """

if __name__ == '__main__':
    # 这里一定要指定host='0.0.0.0'，否则不会监听此端口
    app.run(host='0.0.0.0',port=8888,debug=True)

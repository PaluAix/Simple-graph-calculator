import heapq

# 最短路，直接dijk跑起来
def dijkstra(graph, start):
    # 表存储从起点到该节点的距离，初始化为无穷大
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0  # 起点到自身的距离是0
    # 优先队列
    pq = [(0, start)]
    
    while pq:
        current_distance, current_vertex = heapq.heappop(pq)
        if current_distance > distances[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances

def find_max_edge_path(graph):
    max_weight = 0
    edge = None
    for start in graph:
        for end, weight in graph[start].items():
            if weight > max_weight:
                max_weight = weight
                edge = (start, end)
    return edge, max_weight


def find_shortest_path(graph, start='A', end='B'):
    distances = dijkstra(graph, start)
    path_distance = distances.get(end, "这两点好像还没有修路哦")
    return f"从 {start} 到 {end} 最短只需要走 {path_distance} 步"

def find_longest_path(graph):
    edge, weight = find_max_edge_path(graph)
    if edge:
        return f"从 {edge[0]} 到 {edge[1]} 景点最多，竟然有 {weight} 个！"
    else:
        return "景点太少啦，没什么玩头"

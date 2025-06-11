from flask import Flask, render_template, jsonify, send_from_directory
import os
from queue import PriorityQueue
import math

app = Flask(__name__)

COORDINATES = {
    'hanoi': {'lat': 21.0285, 'lng': 105.8542},
    'hungyen': {'lat': 20.6464, 'lng': 106.0511},
    'bacninh': {'lat': 21.1214, 'lng': 106.1104},
    'hoabinh': {'lat': 20.8135, 'lng': 105.3380},
    'vinhphuc': {'lat': 21.3609, 'lng': 105.5474},
    'haiduong': {'lat': 20.9373, 'lng': 106.3347},
    'haiphong': {'lat': 20.8449, 'lng': 106.6881},
    'quangninh': {'lat': 21.0068, 'lng': 107.2925},
    'bacgiang': {'lat': 21.2717, 'lng': 106.1947},
    'langson': {'lat': 21.8530, 'lng': 106.7610},
    'thainguyen': {'lat': 21.5941, 'lng': 105.8437},
    'backan': {'lat': 22.1477, 'lng': 105.8349},
    'caobang': {'lat': 22.6666, 'lng': 106.2500},
    'tuyenquang': {'lat': 21.7767, 'lng': 105.2280},
    'hagiang': {'lat': 22.8333, 'lng': 104.9833},
    'yenbai': {'lat': 21.7167, 'lng': 104.9000},
    'phutho': {'lat': 21.3200, 'lng': 105.4000},
    'laichau': {'lat': 22.3964, 'lng': 103.4581},
    'dienbien': {'lat': 21.3833, 'lng': 103.0167},
    'sonla': {'lat': 21.3256, 'lng': 103.9191},
    'thaibinh': {'lat': 20.4500, 'lng': 106.3333},
    'namdinh': {'lat': 20.4333, 'lng': 106.1667},
    'ninhbinh': {'lat': 20.2537, 'lng': 105.9754},
    'thanhhoa': {'lat': 19.8066, 'lng': 105.7667},
    'nghean': {'lat': 19.2342, 'lng': 104.9200},
    'hatinh': {'lat': 18.3333, 'lng': 105.9000},
    'quangbinh': {'lat': 17.4667, 'lng': 106.6000},
    'quangtri': {'lat': 16.7500, 'lng': 107.0000},
    'thuathienhue': {'lat': 16.4633, 'lng': 107.5958},
    'danang': {'lat': 16.0544, 'lng': 108.2022},
    'quangnam': {'lat': 15.5793, 'lng': 108.4089},
    'quangngai': {'lat': 15.1213, 'lng': 108.7921},
    'kontum': {'lat': 14.3544, 'lng': 108.0180},
    'binhdinh': {'lat': 14.1667, 'lng': 108.9000},
    'gialai': {'lat': 13.9833, 'lng': 108.0000},
    'phuyen': {'lat': 13.1667, 'lng': 109.1667},
    'daklak': {'lat': 12.6667, 'lng': 108.0500},
    'khanhhoa': {'lat': 12.2500, 'lng': 109.0000},
    'daknong': {'lat': 12.0045, 'lng': 107.6867},
    'lamdong': {'lat': 11.9465, 'lng': 108.4419},
    'ninhthuan': {'lat': 11.7500, 'lng': 108.8333},
    'binhthuan': {'lat': 10.9333, 'lng': 108.1000},
    'binhphuoc': {'lat': 11.7500, 'lng': 106.9167},
    'tayninh': {'lat': 11.3000, 'lng': 106.1000},
    'binhduong': {'lat': 11.1667, 'lng': 106.6667},
    'dongnai': {'lat': 11.1068, 'lng': 107.1678},
    'tphochiminh': {'lat': 10.8231, 'lng': 106.6297},
    'bariavungtau': {'lat': 10.3494, 'lng': 107.0842},
    'longan': {'lat': 10.5417, 'lng': 106.4083},
    'tiengiang': {'lat': 10.3600, 'lng': 106.3600},
    'bentre': {'lat': 10.2417, 'lng': 106.3750},
    'travinh': {'lat': 9.9347, 'lng': 106.3453},
    'vinhlong': {'lat': 10.2537, 'lng': 105.9754},
    'dongthap': {'lat': 10.6667, 'lng': 105.6833},
    'angiang': {'lat': 10.3861, 'lng': 105.4267},
    'kiengiang': {'lat': 10.0167, 'lng': 105.0833},
    'cantho': {'lat': 10.0333, 'lng': 105.7833},
    'haugiang': {'lat': 9.7875, 'lng': 105.4678},
    'soctrang': {'lat': 9.6033, 'lng': 105.9800},
    'baclieu': {'lat': 9.2942, 'lng': 105.7244},
    'camau': {'lat': 9.1769, 'lng': 105.1500},
    'laocai': {'lat': 22.4837, 'lng': 103.9750},
    'hanam': {'lat': 20.5417, 'lng': 105.9225}
}

PROVINCES = {
    'hanoi': {
        'name': 'Hà Nội',
        'representative_number': 24,
        'neighbors': ['hungyen', 'bacninh', 'vinhphuc', 'hoabinh', 'phutho', 'bacgiang','hanam','thainguyen']
    },
    'hungyen': {
        'name': 'Hưng Yên',
        'representative_number': 30,
        'neighbors': ['hanoi', 'bacninh', 'haiduong', 'thaibinh','hanam']
    },
    'bacninh': {
        'name': 'Bắc Ninh',
        'representative_number': 6,
        'neighbors': ['hanoi', 'hungyen', 'haiduong', 'bacgiang']
    },
    'hoabinh': {
        'name': 'Hòa Bình',
        'representative_number': 29,
        'neighbors': ['hanoi', 'phutho', 'sonla', 'thanhhoa','hanam']
    },
    'vinhphuc': {
        'name': 'Vĩnh Phúc',
        'representative_number': 62,
        'neighbors': ['hanoi', 'phutho', 'tuyenquang', 'thainguyen']
    },
    'haiduong': {
        'name': 'Hải Dương',
        'representative_number': 26,
        'neighbors': ['hungyen', 'bacninh', 'bacgiang', 'quangninh', 'haiphong', 'thaibinh']
    },
    'haiphong': {
        'name': 'Hải Phòng',
        'representative_number': 27,
        'neighbors': ['haiduong', 'quangninh', 'thaibinh']
    },
    'quangninh': {
        'name': 'Quảng Ninh',
        'representative_number': 48,
        'neighbors': ['haiduong', 'bacgiang', 'langson', 'haiphong']
    },
    'bacgiang': {
        'name': 'Bắc Giang',
        'representative_number': 3,
        'neighbors': ['hanoi', 'bacninh', 'haiduong', 'quangninh', 'langson', 'thainguyen']
    },
    'langson': {
        'name': 'Lạng Sơn',
        'representative_number': 36,
        'neighbors': ['quangninh', 'bacgiang', 'thainguyen', 'backan', 'caobang']
    },
    'thainguyen': {
        'name': 'Thái Nguyên',
        'representative_number': 54,
        'neighbors': ['vinhphuc', 'bacgiang', 'langson', 'backan', 'tuyenquang','hanoi']
    },
    'backan': {
        'name': 'Bắc Kạn',
        'representative_number': 4,
        'neighbors': ['langson', 'thainguyen', 'tuyenquang', 'caobang']
    },
    'caobang': {
        'name': 'Cao Bằng',
        'representative_number': 14,
        'neighbors': ['langson', 'backan', 'hagiang']
    },
    'tuyenquang': {
        'name': 'Tuyên Quang',
        'representative_number': 60,
        'neighbors': ['vinhphuc', 'thainguyen', 'backan', 'hagiang', 'yenbai', 'phutho']
    },
    'hagiang': {
        'name': 'Hà Giang',
        'representative_number': 22,
        'neighbors': ['caobang', 'backan', 'tuyenquang', 'yenbai','laocai']
    },
    'yenbai': {
        'name': 'Yên Bái',
        'representative_number': 63,
        'neighbors': ['hagiang', 'tuyenquang', 'phutho', 'sonla', 'laichau','laocai']
    },
    'phutho': {
        'name': 'Phú Thọ',
        'representative_number': 43,
        'neighbors': ['hanoi', 'vinhphuc', 'tuyenquang', 'yenbai', 'sonla', 'hoabinh']
    },
    'laichau': {
        'name': 'Lai Châu',
        'representative_number': 34,
        'neighbors': ['yenbai', 'sonla', 'dienbien','laocai']
    },
    'dienbien': {
        'name': 'Điện Biên',
        'representative_number': 18,
        'neighbors': ['laichau', 'sonla']
    },
    'sonla': {
        'name': 'Sơn La',
        'representative_number': 51,
        'neighbors': ['phutho', 'yenbai', 'laichau', 'dienbien', 'thanhhoa', 'hoabinh','laocai']
    },
    'thaibinh': {
        'name': 'Thái Bình',
        'representative_number': 53,
        'neighbors': ['hungyen', 'haiduong', 'haiphong', 'namdinh','hanam']
    },
    'namdinh': {
        'name': 'Nam Định',
        'representative_number': 39,
        'neighbors': ['thaibinh', 'ninhbinh','hanam']
    },
    'ninhbinh': {
        'name': 'Ninh Bình',
        'representative_number': 41,
        'neighbors': ['namdinh', 'thanhhoa', 'hoabinh','hanam']
    },
    'thanhhoa': {
        'name': 'Thanh Hóa',
        'representative_number': 55,
        'neighbors': ['sonla', 'hoabinh', 'ninhbinh', 'nghean']
    },
    'nghean': {
        'name': 'Nghệ An',
        'representative_number': 40,
        'neighbors': ['thanhhoa', 'hatinh']
    },
    'hatinh': {
        'name': 'Hà Tĩnh',
        'representative_number': 25,
        'neighbors': ['nghean', 'quangbinh']
    },
    'quangbinh': {
        'name': 'Quảng Bình',
        'representative_number': 45,
        'neighbors': ['hatinh', 'quangtri']
    },
    'quangtri': {
        'name': 'Quảng Trị',
        'representative_number': 49,
        'neighbors': ['quangbinh', 'thuathienhue']
    },
    'thuathienhue': {
        'name': 'Thừa Thiên Huế',
        'representative_number': 56,
        'neighbors': ['quangtri', 'danang', 'quangnam']
    },
    'danang': {
        'name': 'Đà Nẵng',
        'representative_number': 15,
        'neighbors': ['thuathienhue', 'quangnam']
    },
    'quangnam': {
        'name': 'Quảng Nam',
        'representative_number': 46,
        'neighbors': ['thuathienhue', 'danang', 'quangngai', 'kontum']
    },
    'quangngai': {
        'name': 'Quảng Ngãi',
        'representative_number': 47,
        'neighbors': ['quangnam', 'kontum', 'binhdinh']
    },
    'kontum': {
        'name': 'Kon Tum',
        'representative_number': 33,
        'neighbors': ['quangnam', 'quangngai', 'gialai']
    },
    'binhdinh': {
        'name': 'Bình Định',
        'representative_number': 8,
        'neighbors': ['quangngai', 'gialai', 'phuyen']
    },
    'gialai': {
        'name': 'Gia Lai',
        'representative_number': 21,
        'neighbors': ['kontum', 'binhdinh', 'phuyen', 'daklak']
    },
    'phuyen': {
        'name': 'Phú Yên',
        'representative_number': 44,
        'neighbors': ['binhdinh', 'gialai', 'daklak', 'khanhhoa']
    },
    'daklak': {
        'name': 'Đắk Lắk',
        'representative_number': 16,
        'neighbors': ['gialai', 'phuyen', 'khanhhoa', 'daknong', 'lamdong']
    },
    'khanhhoa': {
        'name': 'Khánh Hòa',
        'representative_number': 31,
        'neighbors': ['phuyen', 'daklak', 'lamdong', 'ninhthuan']
    },
    'daknong': {
        'name': 'Đắk Nông',
        'representative_number': 17,
        'neighbors': ['daklak', 'lamdong', 'binhphuoc']
    },
    'lamdong': {
        'name': 'Lâm Đồng',
        'representative_number': 35,
        'neighbors': ['daklak', 'khanhhoa', 'ninhthuan', 'binhthuan', 'dongnai', 'binhphuoc']
    },
    'ninhthuan': {
        'name': 'Ninh Thuận',
        'representative_number': 42,
        'neighbors': ['khanhhoa', 'lamdong', 'binhthuan']
    },
    'binhthuan': {
        'name': 'Bình Thuận',
        'representative_number': 11,
        'neighbors': ['ninhthuan', 'lamdong', 'dongnai', 'bariavungtau']
    },
    'binhphuoc': {
        'name': 'Bình Phước',
        'representative_number': 10,
        'neighbors': ['daknong', 'lamdong', 'dongnai', 'binhduong', 'tayninh']
    },
    'tayninh': {
        'name': 'Tây Ninh',
        'representative_number': 52,
        'neighbors': ['binhphuoc', 'binhduong', 'longan']
    },
    'binhduong': {
        'name': 'Bình Dương',
        'representative_number': 9,
        'neighbors': ['binhphuoc', 'tayninh', 'tphochiminh', 'dongnai']
    },
    'dongnai': {
        'name': 'Đồng Nai',
        'representative_number': 19,
        'neighbors': ['lamdong', 'binhthuan', 'bariavungtau', 'tphochiminh', 'binhduong', 'binhphuoc']
    },
    'tphochiminh': {
        'name': 'TP Hồ Chí Minh',
        'representative_number': 58,
        'neighbors': ['binhduong', 'dongnai', 'bariavungtau', 'longan', 'tiengiang']
    },
    'bariavungtau': {
        'name': 'Bà Rịa - Vũng Tàu',
        'representative_number': 2,
        'neighbors': ['binhthuan', 'dongnai', 'tphochiminh']
    },
    'longan': {
        'name': 'Long An',
        'representative_number': 38,
        'neighbors': ['tayninh', 'tphochiminh', 'tiengiang', 'dongthap']
    },
    'tiengiang': {
        'name': 'Tiền Giang',
        'representative_number': 57,
        'neighbors': ['tphochiminh', 'longan', 'dongthap', 'vinhlong', 'bentre']
    },
    'bentre': {
        'name': 'Bến Tre',
        'representative_number': 7,
        'neighbors': ['tiengiang', 'vinhlong', 'travinh']
    },
    'travinh': {
        'name': 'Trà Vinh',
        'representative_number': 59,
        'neighbors': ['bentre', 'vinhlong', 'soctrang']
    },
    'vinhlong': {
        'name': 'Vĩnh Long',
        'representative_number': 61,
        'neighbors': ['tiengiang', 'dongthap', 'cantho', 'soctrang', 'travinh', 'bentre']
    },
    'dongthap': {
        'name': 'Đồng Tháp',
        'representative_number': 20,
        'neighbors': ['longan', 'tiengiang', 'vinhlong', 'cantho', 'angiang']
    },
    'angiang': {
        'name': 'An Giang',
        'representative_number': 1,
        'neighbors': ['dongthap', 'cantho', 'kiengiang']
    },
    'kiengiang': {
        'name': 'Kiên Giang',
        'representative_number': 32,
        'neighbors': ['angiang', 'cantho', 'haugiang', 'camau']
    },
    'cantho': {
        'name': 'Cần Thơ',
        'representative_number': 13,
        'neighbors': ['dongthap', 'vinhlong', 'soctrang', 'haugiang', 'kiengiang', 'angiang']
    },
    'haugiang': {
        'name': 'Hậu Giang',
        'representative_number': 28,
        'neighbors': ['cantho', 'soctrang', 'baclieu', 'kiengiang']
    },
    'soctrang': {
        'name': 'Sóc Trăng',
        'representative_number': 50,
        'neighbors': ['travinh', 'vinhlong', 'cantho', 'haugiang', 'baclieu']
    },
    'baclieu': {
        'name': 'Bạc Liêu',
        'representative_number': 5,
        'neighbors': ['soctrang', 'haugiang', 'kiengiang', 'camau']
    },
    'camau': {
        'name': 'Cà Mau',
        'representative_number': 12,
        'neighbors': ['kiengiang', 'baclieu']
    },
    'laocai': {
        'name': 'Lào Cai',
        'representative_number': 37,
        'neighbors': ['laichau', 'hagiang','sonla','yenbai']
    },
    'hanam': {
    'name': 'Hà Nam',
    'representative_number': 23,
    'neighbors': ['hanoi', 'hoabinh', 'ninhbinh', 'namdinh', 'thaibinh','hungyen']
},
    'hoangsa': {
    'name': 'Hoàng Sa',
    'representative_number': 64,
    'neighbors': []
    },
    'truongsa': {
        'name': 'Trường Sa',
        'representative_number': 65,
        'neighbors': []
    },

}

def calculate_distance(coord1, coord2):
    """Tính khoảng cách giữa hai điểm dựa trên tọa độ địa lý"""
    lat1, lng1 = math.radians(coord1['lat']), math.radians(coord1['lng'])
    lat2, lng2 = math.radians(coord2['lat']), math.radians(coord2['lng'])
    
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return c * r

def heuristic(current, goal):
    """Hàm heuristic: ước tính khoảng cách từ điểm hiện tại đến đích"""
    if current not in COORDINATES or goal not in COORDINATES:
        return 0
    return calculate_distance(COORDINATES[current], COORDINATES[goal])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/img/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static', 'img'), filename)

@app.route('/api/provinces')
def get_provinces():
    return jsonify(PROVINCES)

@app.route('/api/path/<start>/<end>')
def find_path(start, end):
    def best_first_search(start, end):
        queue = PriorityQueue()
        queue.put((0, [start]))
        visited = {start}
        
        while not queue.empty():
            current_cost, path = queue.get()
            current = path[-1]

            if current == end:
                return path

            for neighbor in PROVINCES[current]['neighbors']:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    priority = heuristic(neighbor, end)
                    queue.put((priority, new_path))
        
        return None

    path = best_first_search(start, end)
    if path:
        return jsonify({
            'success': True,
            'path': path,
            'path_names': [PROVINCES[p]['name'] for p in path],
            'representative_numbers': [PROVINCES[p]['representative_number'] for p in path]
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Không tìm thấy đường đi'
        })

if __name__ == '__main__':
    app.run(debug=True)

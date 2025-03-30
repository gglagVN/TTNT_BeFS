from flask import Flask, render_template, jsonify, send_from_directory
from collections import deque
import os

app = Flask(__name__)

# Dữ liệu kề của các tỉnh Việt Nam
PROVINCES = {
    'hanoi': {
        'name': 'Hà Nội',
        'representative_number': 23,
        'neighbors': ['hungyen', 'bacninh', 'vinhphuc', 'hoabinh', 'phutho', 'bacgiang']
    },
    'hungyen': {
        'name': 'Hưng Yên',
        'representative_number': 29,
        'neighbors': ['hanoi', 'bacninh', 'haiduong', 'thaibinh']
    },
    'bacninh': {
        'name': 'Bắc Ninh',
        'representative_number': 6,
        'neighbors': ['hanoi', 'hungyen', 'haiduong', 'bacgiang']
    },
    'hoabinh': {
        'name': 'Hòa Bình',
        'representative_number': 28,
        'neighbors': ['hanoi', 'phutho', 'sonla', 'thanhhoa']
    },
    'vinhphuc': {
        'name': 'Vĩnh Phúc',
        'representative_number': 60,
        'neighbors': ['hanoi', 'phutho', 'tuyenquang', 'thainguyen', 'bacgiang']
    },
    'haiduong': {
        'name': 'Hải Dương',
        'representative_number': 25,
        'neighbors': ['hungyen', 'bacninh', 'bacgiang', 'quangninh', 'haiphong', 'thaibinh']
    },
    'haiphong': {
        'name': 'Hải Phòng',
        'representative_number': 26,
        'neighbors': ['haiduong', 'quangninh', 'thaibinh']
    },
    'quangninh': {
        'name': 'Quảng Ninh',
        'representative_number': 46,
        'neighbors': ['haiduong', 'bacgiang', 'langson', 'haiphong']
    },
    'bacgiang': {
        'name': 'Bắc Giang',
        'representative_number': 3,
        'neighbors': ['hanoi', 'bacninh', 'haiduong', 'quangninh', 'langson', 'thainguyen', 'vinhphuc']
    },
    'langson': {
        'name': 'Lạng Sơn',
        'representative_number': 35,
        'neighbors': ['quangninh', 'bacgiang', 'thainguyen', 'backan', 'caobang']
    },
    'thainguyen': {
        'name': 'Thái Nguyên',
        'representative_number': 52,
        'neighbors': ['vinhphuc', 'bacgiang', 'langson', 'backan', 'tuyenquang']
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
        'representative_number': 58,
        'neighbors': ['vinhphuc', 'thainguyen', 'backan', 'hagiang', 'yenbai', 'phutho']
    },
    'hagiang': {
        'name': 'Hà Giang',
        'representative_number': 22,
        'neighbors': ['caobang', 'backan', 'tuyenquang', 'yenbai']
    },
    'yenbai': {
        'name': 'Yên Bái',
        'representative_number': 61,
        'neighbors': ['hagiang', 'tuyenquang', 'phutho', 'sonla', 'laichau']
    },
    'phutho': {
        'name': 'Phú Thọ',
        'representative_number': 41,
        'neighbors': ['hanoi', 'vinhphuc', 'tuyenquang', 'yenbai', 'sonla', 'hoabinh']
    },
    'laichau': {
        'name': 'Lai Châu',
        'representative_number': 33,
        'neighbors': ['yenbai', 'sonla', 'dienbien']
    },
    'dienbien': {
        'name': 'Điện Biên',
        'representative_number': 18,
        'neighbors': ['laichau', 'sonla']
    },
    'sonla': {
        'name': 'Sơn La',
        'representative_number': 49,
        'neighbors': ['phutho', 'yenbai', 'laichau', 'dienbien', 'thanhhoa', 'hoabinh']
    },
    'thaibinh': {
        'name': 'Thái Bình',
        'representative_number': 51,
        'neighbors': ['hungyen', 'haiduong', 'haiphong', 'namdinh']
    },
    'namdinh': {
        'name': 'Nam Định',
        'representative_number': 37,
        'neighbors': ['thaibinh', 'ninhbinh', 'thanhhoa']
    },
    'ninhbinh': {
        'name': 'Ninh Bình',
        'representative_number': 39,
        'neighbors': ['namdinh', 'thanhhoa', 'hoabinh']
    },
    'thanhhoa': {
        'name': 'Thanh Hóa',
        'representative_number': 53,
        'neighbors': ['sonla', 'hoabinh', 'ninhbinh', 'nghean']
    },
    'nghean': {
        'name': 'Nghệ An',
        'representative_number': 38,
        'neighbors': ['thanhhoa', 'hatinh']
    },
    'hatinh': {
        'name': 'Hà Tĩnh',
        'representative_number': 24,
        'neighbors': ['nghean', 'quangbinh']
    },
    'quangbinh': {
        'name': 'Quảng Bình',
        'representative_number': 43,
        'neighbors': ['hatinh', 'quangtri']
    },
    'quangtri': {
        'name': 'Quảng Trị',
        'representative_number': 47,
        'neighbors': ['quangbinh', 'thuathienhue']
    },
    'thuathienhue': {
        'name': 'Thừa Thiên Huế',
        'representative_number': 54,
        'neighbors': ['quangtri', 'danang', 'quangnam']
    },
    'danang': {
        'name': 'Đà Nẵng',
        'representative_number': 15,
        'neighbors': ['thuathienhue', 'quangnam']
    },
    'quangnam': {
        'name': 'Quảng Nam',
        'representative_number': 44,
        'neighbors': ['thuathienhue', 'danang', 'quangngai', 'kontum']
    },
    'quangngai': {
        'name': 'Quảng Ngãi',
        'representative_number': 45,
        'neighbors': ['quangnam', 'kontum', 'binhdinh']
    },
    'kontum': {
        'name': 'Kon Tum',
        'representative_number': 32,
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
        'representative_number': 42,
        'neighbors': ['binhdinh', 'gialai', 'daklak', 'khanhhoa']
    },
    'daklak': {
        'name': 'Đắk Lắk',
        'representative_number': 16,
        'neighbors': ['gialai', 'phuyen', 'khanhhoa', 'daknong', 'lamdong']
    },
    'khanhhoa': {
        'name': 'Khánh Hòa',
        'representative_number': 30,
        'neighbors': ['phuyen', 'daklak', 'lamdong', 'ninhthuan']
    },
    'daknong': {
        'name': 'Đắk Nông',
        'representative_number': 17,
        'neighbors': ['daklak', 'lamdong', 'binhphuoc']
    },
    'lamdong': {
        'name': 'Lâm Đồng',
        'representative_number': 34,
        'neighbors': ['daklak', 'khanhhoa', 'ninhthuan', 'binhthuan', 'dongnai', 'binhphuoc']
    },
    'ninhthuan': {
        'name': 'Ninh Thuận',
        'representative_number': 40,
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
        'representative_number': 50,
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
        'representative_number': 56,
        'neighbors': ['binhduong', 'dongnai', 'bariavungtau', 'longan', 'tiengiang']
    },
    'bariavungtau': {
        'name': 'Bà Rịa - Vũng Tàu',
        'representative_number': 2,
        'neighbors': ['binhthuan', 'dongnai', 'tphochiminh']
    },
    'longan': {
        'name': 'Long An',
        'representative_number': 36,
        'neighbors': ['tayninh', 'tphochiminh', 'tiengiang', 'dongthap']
    },
    'tiengiang': {
        'name': 'Tiền Giang',
        'representative_number': 55,
        'neighbors': ['tphochiminh', 'longan', 'dongthap', 'vinhlong', 'bentre']
    },
    'bentre': {
        'name': 'Bến Tre',
        'representative_number': 7,
        'neighbors': ['tiengiang', 'vinhlong', 'travinh']
    },
    'travinh': {
        'name': 'Trà Vinh',
        'representative_number': 57,
        'neighbors': ['bentre', 'vinhlong', 'soctrang']
    },
    'vinhlong': {
        'name': 'Vĩnh Long',
        'representative_number': 59,
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
        'representative_number': 31,
        'neighbors': ['angiang', 'cantho', 'haugiang', 'camau']
    },
    'cantho': {
        'name': 'Cần Thơ',
        'representative_number': 13,
        'neighbors': ['dongthap', 'vinhlong', 'soctrang', 'haugiang', 'kiengiang', 'angiang']
    },
    'haugiang': {
        'name': 'Hậu Giang',
        'representative_number': 27,
        'neighbors': ['cantho', 'soctrang', 'baclieu', 'kiengiang']
    },
    'soctrang': {
        'name': 'Sóc Trăng',
        'representative_number': 48,
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
    'representative_number': 33,  
    'neighbors': ['hanoi', 'hoabinh', 'ninhbinh', 'namdinh', 'thaibinh']
},

}

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
    def bfs(start, end):
        queue = deque([[start]])
        visited = {start}
        
        while queue:
            path = queue.popleft()
            current = path[-1]
            
            if current == end:
                return path
                
            for neighbor in PROVINCES[current]['neighbors']:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        
        return None

    path = bfs(start, end)
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
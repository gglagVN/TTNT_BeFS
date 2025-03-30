document.addEventListener('DOMContentLoaded', function() {
    const svgObject = document.getElementById('vietnam-map');
    const startSelect = document.getElementById('startProvince');
    const endSelect = document.getElementById('endProvince');
    let provinces = {};

    // Lấy danh sách tỉnh từ API
    fetch('/api/provinces')
        .then(response => response.json())
        .then(data => {
            provinces = data;
            populateSelects(data);
        });

    // Xử lý khi SVG load xong
    svgObject.addEventListener('load', function() {
        const svgDoc = svgObject.contentDocument;
        
        // Thêm sự kiện click cho các tỉnh
        const provinceElements = svgDoc.querySelectorAll('.province');
        provinceElements.forEach(province => {
            province.addEventListener('click', function(e) {
                const provinceId = this.id;
                handleProvinceClick(provinceId);
            });
        });
    });

    // Điền dữ liệu vào các dropdown
    function populateSelects(provinces) {
        const sortedProvinces = Object.entries(provinces)
            .sort((a, b) => a[1].name.localeCompare(b[1].name));

        sortedProvinces.forEach(([id, data], index) => {
            const option = new Option(`${index + 1}. ${data.name}`, id);
            startSelect.add(option.cloneNode(true));
            endSelect.add(option);
        });
    }

    // Xử lý khi click vào tỉnh trên bản đồ
    function handleProvinceClick(provinceId) {
        if (!startSelect.value) {
            startSelect.value = provinceId;
        } else if (!endSelect.value && provinceId !== startSelect.value) {
            endSelect.value = provinceId;
            document.getElementById('pathForm').dispatchEvent(new Event('submit'));
        }
        updateMapSelection();
    }

    // Cập nhật hiển thị trên bản đồ
    function updateMapSelection() {
        const svgDoc = svgObject.contentDocument;
        svgDoc.querySelectorAll('.province').forEach(province => {
            province.classList.remove('selected', 'path');
        });

        if (startSelect.value) {
            const startProvince = svgDoc.getElementById(startSelect.value);
            if (startProvince) startProvince.classList.add('selected');
        }
        
        if (endSelect.value) {
            const endProvince = svgDoc.getElementById(endSelect.value);
            if (endProvince) endProvince.classList.add('selected');
        }
    }

    // Xử lý form submit
    document.getElementById('pathForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const start = startSelect.value;
        const end = endSelect.value;
        
        if (start && end) {
            fetch(`/api/path/${start}/${end}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        displayPath(data.path, data.path_names, data.representative_numbers);
                    } else {
                        displayError('Không tìm thấy đường đi');
                    }
                });
        }
    });

    // Hiển thị đường đi
    function displayPath(path, pathNames, representativeNumbers) {
        const svgDoc = svgObject.contentDocument;
        
        // Xóa đường đi cũ
        svgDoc.querySelectorAll('.province.path').forEach(province => {
            province.classList.remove('path');
        });
        
        // Thêm đường đi mới
        path.forEach(provinceId => {
            const province = svgDoc.getElementById(provinceId);
            if (province) {
                province.classList.add('path');
            }
        });
        
        // Hiển thị kết quả
        document.getElementById('path-display').innerHTML = 
            pathNames.map((name, index) => `${index + 1}. ${name}`).join(' → ');
        document.getElementById('distance-display').innerHTML = 
            `Số tỉnh phải đi qua: ${path.length - 1}`;
        document.getElementById('representative-numbers').innerHTML = 
            `Số đại diện: ${representativeNumbers.join(', ')}`;
    }

    // Hiển thị lỗi
    function displayError(message) {
        document.getElementById('result').innerHTML = 
            `<div class="alert alert-warning">${message}</div>`;
    }

    // Xử lý nút đặt lại
    document.getElementById('resetBtn').addEventListener('click', function() {
        startSelect.value = '';
        endSelect.value = '';
        document.getElementById('result').innerHTML = '';
        const svgDoc = svgObject.contentDocument;
        svgDoc.querySelectorAll('.province').forEach(province => {
            province.classList.remove('selected', 'path');
        });
    });

    // Xử lý thay đổi dropdown
    startSelect.addEventListener('change', updateMapSelection);
    endSelect.addEventListener('change', updateMapSelection);
});
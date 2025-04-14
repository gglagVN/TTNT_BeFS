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
        const entries = Object.entries(provinces);
    
        const mainProvinces = [];
        const extraProvinces = [];
    
        entries.forEach(([id, data]) => {
            // Giả sử các tỉnh phụ có id đặc biệt
            if (["hoangsa", "truongsa"].includes(id.toLowerCase())) {
                extraProvinces.push([id, data]);
            } else {
                mainProvinces.push([id, data]);
            }
        });
    
        // Sort riêng từng nhóm theo tên
        mainProvinces.sort((a, b) => a[1].name.localeCompare(b[1].name));
        extraProvinces.sort((a, b) => a[1].name.localeCompare(b[1].name));
    
        // Gộp lại: chính trước, phụ sau
        const finalList = [...mainProvinces, ...extraProvinces];
    
        finalList.forEach(([id, data], index) => {
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
        // Reset các dropdown
        startSelect.value = '';
        endSelect.value = '';
        
        // Xóa kết quả
        clearResults();
        
        // Xóa đường đi trên bản đồ
        const svgDoc = svgObject.contentDocument;
        if (svgDoc) {
            // Xóa tất cả các class được thêm vào các tỉnh
            svgDoc.querySelectorAll('.province').forEach(province => {
                province.classList.remove('selected', 'path');
            });
        }
        
        // Clear any existing error messages
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => alert.remove());
    });
    function clearResults() {
        const resultDiv = document.getElementById('result');
        if(resultDiv) {
            // Xóa toàn bộ nội dung trong div result
            resultDiv.innerHTML = '';
            
            // Tạo lại cấu trúc div rỗng để sẵn sàng cho kết quả mới
            resultDiv.innerHTML = `
                <div id="path-display"></div>
                <div id="distance-display" class="mt-2"></div>
                <div id="representative-numbers" class="mt-2"></div>
            `;
        }
    }

    // Xử lý thay đổi dropdown
    startSelect.addEventListener('change', updateMapSelection);
    endSelect.addEventListener('change', updateMapSelection);
});
function updateMapSelection() {
    const svgDoc = svgObject.contentDocument;
    if (!svgDoc) return;

    // Xóa tất cả các lớp selected và path
    clearSelections(svgDoc);

    // Thêm lớp selected cho các tỉnh được chọn
    if (startSelect.value) {
        const startProvince = svgDoc.getElementById(startSelect.value);
        if (startProvince) startProvince.classList.add('selected');
    }
    
    if (endSelect.value) {
        const endProvince = svgDoc.getElementById(endSelect.value);
        if (endProvince) endProvince.classList.add('selected');
    }
}

function clearSelections(svgDoc) {
    const provinces = svgDoc.querySelectorAll('.province');
    provinces.forEach(province => {
        province.classList.remove('selected', 'path');
    });
};

// ドラッグ&ドロップエリアの取得
var fileArea = document.getElementById('dropArea');

// input[type=file]の取得
var fileInput = document.getElementById('uploadFile');
var fileSubmit = document.getElementById('submitFile');

// ファイルアップロードボタンを取得
var btnInputFile = document.getElementById('btnInputFile')

// 送信ボタンを取得
var btnUploadFile = document.getElementById('btnUploadFile')

// ドラッグオーバー時の処理
fileArea.addEventListener('dragover', function(e) {
    e.preventDefault();
    fileArea.classList.add('dragover');
});

// ドラッグアウト時の処理
fileArea.addEventListener('dragleave', function(e) {
    e.preventDefault();
    fileArea.classList.remove('dragover');
});

// ドロップ時の処理
fileArea.addEventListener('drop', function(e) {
    e.preventDefault();
    fileArea.classList.remove('dragover');

    // ドロップしたファイルの取得
    var files = e.dataTransfer.files;

    // 取得したファイルをinput[type=file]へ
    fileInput.files = files;

    if(typeof files[0] !== 'undefined') {
        //ファイルが正常に受け取れた際の処理
        // ファイル名を出力
        fileArea.innerHTML = 'Drop PDF File Here.<br><span class="text-info">' + files[0].name + '</span>';
        // 選択用のボタンを非表示
        btnInputFile.style.display = 'none';
        fileInput.style.display = 'none'
        // 送信用ボタンを表示
        btnUploadFile.style.display = 'table';
        fileSubmit.style.display = 'block'

    } else {
        //ファイルが受け取れなかった際の処理
        // ファイルが受け取れなかった胸を出力
        fileArea.textContent = 'File could not be received. Please upload again.';
    }

});

// ファイル内容が変更された時の処理
fileInput.addEventListener('change', function(e){
    var files = e.target.files;
    fileInput.files = files;
    if(typeof files[0] !== 'undefined') {
        //ファイルが正常に受け取れた際の処理
        // ファイル名を出力
        fileArea.innerHTML = 'Drop PDF File Here.<br><span class="text-info">' + files[0].name + '</span>';
        // 選択用のボタンを非表示
        btnInputFile.style.display = 'none';
        fileInput.style.display = 'none'
        // 送信用ボタンを表示
        btnUploadFile.style.display = 'table';
        fileSubmit.style.display = 'block'

    } else {
        //ファイルが受け取れなかった際の処理
        // ファイルが受け取れなかった胸を出力
        fileArea.textContent = 'File could not be received. Please upload again.';
    }
}, false);
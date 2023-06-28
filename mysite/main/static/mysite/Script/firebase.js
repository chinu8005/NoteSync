const firebaseConfig = {
    apiKey: "AIzaSyA0U8lSsP8EgO-MnwkopeLbokCb5fhJna0",
    authDomain: "notesync-2184.firebaseapp.com",
    databaseURL: "https://notesync-2184-default-rtdb.firebaseio.com",
    projectId: "notesync-2184",
    storageBucket: "notesync-2184.appspot.com",
    messagingSenderId: "436756773807",
    appId: "1:436756773807:web:4b285eec661059027c8d5a",
    measurementId: "G-Z3WN96RBBK"
    };

    firebase.initializeApp(firebaseConfig);
    var fileItem;
    var fileName;
    
    function getFile(e){
        fileItem = e.target.files[0];
        fileName = fileItem.name;
        console.log(fileItem)
        console.log(fileName)
    }
    function uploadPDF(){


        const storageRef = firebase.storage().ref();
        const pdfRef = storageRef.child("PDFs/"+fileName);


        const task = pdfRef.put(fileItem)

        task.then(snapshot => {
            snapshot.ref.getDownloadURL().then(url => {
                document.getElementById('pdfuploadurl').value = url;
                document.getElementById('title-input').value = document.getElementById('title').value;
                document.getElementById('subject-input').value = document.getElementById('subject').value;
                document.getElementById('description-input').value = document.getElementById('discription').value;
                document.getElementById('uploadnotes').click();
                
            })
        })
    }
    

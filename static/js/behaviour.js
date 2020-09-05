$("#file").on("change", function(evt) {


    var file = evt.target.files[0];

    //Read the file using file reader
    var fileReader = new FileReader();

    fileReader.onload = function() {

        //Turn array buffer into typed array
        var typedarray = new Uint8Array(this.result);

        //calling function to read from pdf file
        getText(typedarray).then(function(text) {

                /*Selected pdf file content is in the variable text. */
                $("#content").html(text);
            }, function(reason) //Execute only when there is some error while reading pdf file
            {
                alert('Seems this file is broken, please upload another file');
                console.error(reason);
            });

        //getText() function definition. This is the pdf reader function.
        function getText(typedarray) {

            //PDFJS should be able to read this typedarray content

            var pdf = PDFJS.getDocument(typedarray);
            return pdf.then(function(pdf) {

                // get all pages text
                var maxPages = pdf.pdfInfo.numPages;
                var countPromises = [];
                // collecting all page promises
                for (var j = 1; j <= maxPages; j++) {
                    var page = pdf.getPage(j);

                    var txt = "";
                    countPromises.push(page.then(function(page) {
                        // add page promise
                        var textContent = page.getTextContent();

                        return textContent.then(function(text) {
                            // return content promise
                            return text.items.map(function(s) {
                                return s.str;
                            }).join(''); // value page text
                        });
                    }));
                }

                // Wait for all pages and join text
                return Promise.all(countPromises).then(function(texts) {
                    return texts.join('');
                });
            });
        }
    };
    //Read the file as ArrayBuffer
    fileReader.readAsArrayBuffer(file);

});
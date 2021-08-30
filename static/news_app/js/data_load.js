$(document).ready(function () {
    // console.log("ready!");
    element = document.getElementsByClassName("text-muted")
    for (i = 0; i < element.length; i++) {
        t = element[i].innerText
        var d = new Date(t)
        element[i].innerText = d.toDateString()
    }
});

var page = 2;
var window_scroll = true;
var search = "{{ search }}";

window.addEventListener('scroll', function (e) {
    // scroll check
    // console.log("scroll check...")
    $(document).ready(function () {
        element = document.getElementsByClassName("text-muted")
        for (i = 0; i < element.length; i++) {
            t = element[i].innerText
            var d = new Date(t)
            element[i].innerText = d.toDateString()
        }
    });
    if (window_scroll) {
        if ((window.innerHeight + window.scrollY) >= (document.body.scrollHeight - 200)) {
            window_scroll = false;
            document.getElementById("loading").style.display = "block";
            $.ajax({
                url: '/next?page=' + page + '&search=' + search,
                dataType: 'json',
                success: function (data) {
                    if (data["success"]) {
                        articles = data["data"]
                        articles_html = ''
                        for (i = 0; i < articles.length; i++) {
                            articles_html += ' \
                            <div class="card mb-3 box" style="margin:auto;">\
                                <div class="row">\
                                    <div class="col-md-8">\
                                        <div class="card-body">\
                                            <h5 class="card-title"><a href="'+ articles[i]["url"] + '" target="_blanck" class="text-decoration-none">' + articles[i]["title"] + '</a></h5>\
                                            <p class="card-text">Source: '+ articles[i]["source"] + '</p>\
                                            <p class="card-text">Author: '+ articles[i]["author"] + '</p>\
                                            <p class="card-text"><small class="text-muted">'+ articles[i]["publishedAt"] + '</small></p>\
                                            <p class="card-text">'+ articles[i]["description"] + '</p>\
                                        </div>\
                                    </div>\
                                            \
                                    <div class="col-md-4 img-box">\
                                        <img src="'+ articles[i]["image"] + '" class="card-img" alt="..." height="100%">\
                                    </div>\
                                </div>\
                            </div>\
                            '
                        }
                        $("#articles-container").append(articles_html);
                        page += 1
                        window_scroll = true;
                        document.getElementById("loading").style.display = "none";
                    }
                    else {
                        // console.log("Failed")
                        window_scroll = true;
                        document.getElementById("loading").style.display = "none";
                    }
                }
            });
        }
    }
})

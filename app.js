var http = require("http");
var fs = require("fs");

var server = http.createServer(function(req, res) {
	fs.readFile("index.html","utf8" , function(err, page) {
		if(err) {
			throw err;
		}
		var my_data = JSON.stringify(get_data());
		page = page.replace("##MY_DATA##", my_data);
		res.writeHead(200, {"Content-type":"text/html"})
		res.write(page);
		res.end();
	});	
});

server.listen(8080);

function get_data() {
	var data_json = JSON.parse(fs.readFileSync("./log_file.json", "utf8"));

	date = data_json["date"];
	s1 = data_json["sensor1"];
	s2 = data_json["sensor2"];
	s3 = data_json["sensor3"];
	s4 = data_json["sensor4"];

	return [date, s1, s2, s3, s4];
}

const http = require("http");
const url = require("url");

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  const method = req.method;

  // Helper to send JSON response
  function sendJSON(statusCode, body) {
    const payload = JSON.stringify(body, null, 2);
    res.writeHead(statusCode, {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(payload)
    });
    res.end(payload);
  }

  // Helper to send empty response
  function sendEmpty(statusCode) {
    res.writeHead(statusCode, {});
    res.end();
  }

  // Route: GET /vehicles
  // @endpoint GET /vehicles
  if (method === "GET" && pathname === "/vehicles") {
    sendJSON(200, [
      {
        "id": 1,
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": 159864
      },
      {
        "id": 2,
        "nickName": "Dolly",
        "vin": "JN8AZ2KR1AT169594",
        "make": "Nissan",
        "model": "Cube",
        "year": "2010",
        "miles": 59000
      }
    ]);
    return;
  }

  // Route: POST /vehicles
  // @endpoint POST /vehicles
  if (method === "POST" && pathname === "/vehicles") {
    let body = "";
    req.on("data", chunk => { body += chunk; });
    req.on("end", () => {
      sendJSON(201, {
        "id": 1,
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": "159,864"
      });
    });
    return;
  }

  // Route: GET /vehicles/:id
  // @endpoint GET /vehicles/:id
  const vehicleByIdMatch = pathname.match(/^\/vehicles\/(\d+)$/);
  if (method === "GET" && vehicleByIdMatch) {
    const id = parseInt(vehicleByIdMatch[1]);
    if (id === 1) {
      sendJSON(200, {
        "id": 1,
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": 159864
      });
    } else {
      sendJSON(404, {
        "error": "Not found",
        "message": `Vehicle with id ${id} not found`
      });
    }
    return;
  }

  // Route: PATCH /vehicles/:id
  // @endpoint PATCH /vehicles/:id
  if (method === "PATCH" && vehicleByIdMatch) {
    let body = "";
    req.on("data", chunk => { body += chunk; });
    req.on("end", () => {
      let parsed = {};
      try { parsed = JSON.parse(body); } catch (e) {}
      sendJSON(200, Object.assign({
        "id": 1,
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": 159999
      }, parsed, { id: parseInt(vehicleByIdMatch[1]) }));
    });
    return;
  }

  // Route: DELETE /vehicles/:id
  // @endpoint DELETE /vehicles/:id
  if (method === "DELETE" && vehicleByIdMatch) {
    sendEmpty(204);
    return;
  }

  // 404 fallback
  sendJSON(404, { "error": "Not found", "message": "The requested endpoint does not exist." });
});

server.listen(process.env.PORT || 4501);

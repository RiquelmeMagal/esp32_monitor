#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include "DHTesp.h"

DHTesp dht;

const char* ssid = "NOME DA SUA REDE";
const char* password = "SENHA DA SUA REDE";

WebServer server(80);

void handleRoot() {
  String umidade = String(dht.getHumidity());
  String temperatura = String(dht.getTemperature());
 
  server.send(200, "text/plain", umidade + "e" + temperatura);  // 70.0e23.0
}

void handleData() {
  String umidade = String(dht.getHumidity());
  String temperatura = String(dht.getTemperature());

  String json = "{\"umidade\":\"" + umidade + "\",\"temperatura\":\"" + temperatura + "\"}";
  server.send(200, "application/json", json);
}

void handleNotFound() {
  String message = "File Not Found\n";
  server.send(404, "text/plain", message);
}

void setup(void) {
  dht.setup(4, DHTesp::DHT11); // D4
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp32")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", HTTP_GET, handleRoot);
  server.on("/data", HTTP_GET, handleData); // Adicionado o manipulador para a rota /data
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
}

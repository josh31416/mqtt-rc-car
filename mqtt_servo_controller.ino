// LIBRARIES
// ==========================
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>
// ==========================

// CONSTANTS
// ==========================
const char* ssid = "WLAN_PI";
const char* password = "";
const char* mqtt_server = "192.168.10.1";
// ==========================

// Initialize variables
Servo sterringServo;
Servo throttleServo;
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

// Arduino setup function
void setup() {
  // Attach sterring servo to D4 pin
  sterringServo.attach(2);
  delay(1000);
  // Initialize servo degrees
  sterringServo.write(90);
  // Attach throttle servo to D5 pin
  throttleServo.attach(14);
  delay(1000);
  // Initialize servo degrees
  throttleServo.write(90);
  delay(2000);
  // Initialize serial for monitoring
  Serial.begin(115200);
  // Setup wifi
  setup_wifi();
  // Setup mqtt client
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}
 
void setup_wifi() {
  delay(10);
  Serial.print("\nConnecting to ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

// MQTT callback function
void callback(char* topic, byte* payload, unsigned int length) {
  int degrees = 0;
  for (int i = 0; i < length; i++) {
    degrees += pow(10, length-1-i)*(String((char) payload[i]).toInt());
  }
  Serial.println(degrees);
  if (strcmp(topic, "servo/sterring") == 0){
    sterringServo.write(degrees);
  }
  if (strcmp(topic, "servo/throttle") == 0){
    throttleServo.write(degrees);
  }
  
}

// MQTT reconnect function
void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP8266Client", "josh", "")) {
      Serial.println("connected");
      client.subscribe("servo/sterring");
      client.subscribe("servo/throttle");
    } else {
      delay(5000);
    }
  }
}

// Arduino loop function
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

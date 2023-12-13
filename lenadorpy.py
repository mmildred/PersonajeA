from machine import Pin, PWM
from hcsr04 import HCSR04
from time import sleep
from umqtt.simple import MQTTClient
import network
import _thread




#Definimos las propiedades de conexion con el servidor
MQTT_BROKER = "broker.hivemq.com"
MQTT_CLIENT_ID = ""
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC = "utng/eaza/led"
MQTT_PORT = 1883

#Funcion para conexion wifi
def conectar_wifi():
    print("Conectando...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("UTNG_Alumnos","")
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("Wifi conectada!")

#funcion para encender y apagar led

def llegada_mensaje(topic, msg):
    print("mensaje: ", msg)
    if msg == b'1':
        ledPin3.value(1)
    elif msg==b'0':
        ledPin3.value(0)
    if msg == b'sirve':
        ledPin2.value(not ledPin2.value())
        for i in range(1800, 4000, 200):
            servo2.duty_u16(i)
            ledPin2.value(1)
            sleep(0.1)


    elif msg==b'nosirve':
        for i in range(4000, 1800, -200):
            servo2.duty_u16(i)
            ledPin2.value(0)
            sleep(0.1)

    else:
        print("Mensaje no valido")    
        




def subscribir():
    client=MQTTClient(MQTT_CLIENT_ID,MQTT_BROKER,port=MQTT_PORT,user=MQTT_USER, password=MQTT_PASSWORD,keepalive=0)

    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Conectando a: ", MQTT_BROKER, "en el topico",MQTT_TOPIC)
    return client

                        

conectar_wifi()


client=subscribir()



ledPin = Pin(13, Pin.OUT)
ledPin2 = Pin(19, Pin.OUT)
ledPin3 = Pin(21, Pin.OUT)

# Servo motor
servo = PWM(Pin(15), freq=50)
servo2 = PWM(Pin(4), freq=50)

# Creamos el objeto HCSR04
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=24000)

# Inicio del zumbador
buzzer = PWM(Pin(2), freq=440, duty=0)  # Inicialmente, el zumbador está apagado

# Define el tono de Spider-Man
spiderman_melody = [
    (330, 0.2),  # Mi
    (349, 0.2),  # Fa
    (392, 0.2),  # Sol
    (330, 0.2),  # Mi
    (392, 0.2),  # Sol
    (330, 0.2),  # Mi
    (294, 0.2),  # Re
    (330, 0.2),  # Mi
    (349, 0.2),  # Fa
    (392, 0.2),  # Sol
    (330, 0.2),  # Mi
    (294, 0.2),  # Re
    (330, 0.2),  # Mi
    (330, 0.2),  # Mi
    (349, 0.2),  # Fa
    (392, 0.2),  # Sol
    (440, 0.2),  # La
    (392, 0.2),  # Sol
    (349, 0.2),  # Fa
    (330, 0.2),  # Mi
]

# Define otra melodía
other_melody = [
    (262, 0.2),  # Do
    (294, 0.2),  # Re
    (330, 0.2),  # Mi
    (349, 0.2),  # Fa
    (392, 0.2),  # Sol
]

# Función para tocar una melodía
def play_melody(melody, tempo):
    for note in melody:
        frequency, duration = note
        buzzer.freq(frequency)
        buzzer.duty(512)
        sleep(duration * tempo)
    buzzer.duty(0)


def ejecutar_logica():
    distancia = sensor.distance_cm()
    print("Distancia:", distancia, "centímetros")


    if distancia <= 100:
        ledPin.value(not ledPin.value())

        for i in range(1800, 8000, 200):
            servo.duty_u16(i)
            sleep(0.1)
        play_melody(spiderman_melody, 0.8)

        for i in range(8000, 1800, -200):
            servo.duty_u16(i)
            sleep(0.1)
        ledPin.value(not ledPin.value())

    else:
        play_melody(other_melody, 0.8)
        buzzer.duty(0)
        ledPin.value(ledPin.value())
        

    sleep(1)


def ejecutar_logica_thread():
    while True:
        ejecutar_logica()

# Inicia el hilo para la lógica
_thread.start_new_thread(ejecutar_logica_thread, ())

# Bucle principal
while True:
    client.wait_msg()
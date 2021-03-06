import mqtt
import config
import threading


class MQTTAdapter():
    def __init__(self):
        self.mqtt = mqtt.MQTT()
        self.__init()

    def __init(self):
        self.__thread_condition = threading.Condition()

        t = threading.Thread(target=self.__subscribe)
        t.start()

    def getMessage(self):
        with self.__thread_condition:
            self.__thread_condition.wait()
        return self.__dict['type'], self.__dict['data']

    def __subscribeCallback(self, _dict):
        self.__dict = _dict
        with self.__thread_condition:
            self.__thread_condition.notify()

    def __subscribe(self):
        self.mqtt.subscribe(
            config.MQTT['topic_device'], 0, self.__subscribeCallback)

    def subscribe_receiving(self, _callback):
        def subscribe_receiving_callback(_dict):
            _callback(_dict)
        self.mqtt.subscribe(
            config.MQTT['topic_device_data'], 0, subscribe_receiving_callback)

    def close(self):
        self.mqtt.disconnect()

    def sendData(self, _idx, _power, _sound):
        # 데이터 포맷맞추기 필요.
        self.mqtt.publish(config.MQTT['topic_sheet_log'], {
                          "sheet_use_idx": _idx, "power": _power, "sound": _sound}, 0)

    def sendRfidData(self, _rfid_id):
        print({
            "sheet_idx": config.index, "rfid_id": _rfid_id
        })
        self.mqtt.publish(config.MQTT['topic_device_rfid'], {
            "sheet_idx": config.index, "rfid_id": _rfid_id
        }, 0)


if __name__ == "__main__":
    '''
    def testCallback(_type, _idx):
        print("type : "+str(_type)+" idx : "+str(_idx))
    ma = MQTTAdapter(testCallback)
    for i in range(20000000):
        pass

    ma.close()
    '''

    ma = MQTTAdapter()
    _type, _data = ma.getMessage()
    print(str(_type)+" / "+str(_data))
    _type, _data = ma.getMessage()
    print(str(_type)+" / "+str(_data))
    _type, _data = ma.getMessage()
    print(str(_type)+" / "+str(_data))
    ma.close()

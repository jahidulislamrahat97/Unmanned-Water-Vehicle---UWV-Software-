import paho.mqtt.client as mqtt


class MqttClient():
    def __init__(self, id:str = None, use_id_as_client_id:bool = False, 
                 client_id:str = None, clean_session:bool = None, 
                 userdata = None, protocol:int = mqtt.MQTTv311, 
                 transport:str = 'tcp', reconnect_on_failure:bool = True) -> None:
        '''
        id is the ID of the device in string format.
        Pass this while creating the object or later with the method.
        In case of passing the id later, use_id_as_client_id will be False.
        
        use_id_as_client_id is a boolean that determines whether the
        id you passed will be used as MQTT client id or not.
        Keep in mind, if multiple client under the same broker exists,
        they will be continuously disconnected.
        
        Reset of it is excatly doing what mqtt.Client does, 
        except the client will be an object of this class.
        Here's the details,
        
        client_id is the unique client id string used when connecting to the broker. 
        If client_id is zero length or None, then the behaviour is defined by which 
        protocol version is in use. If using MQTT v3.1.1, then a zero length client id 
        will be sent to the broker and the broker will generate a random for the client. 
        If using MQTT v3.1 then an id will be randomly generated. 
        In both cases, clean_session must be True. If this is not the case a ValueError will be raised.
        
        clean_session is a boolean that determines the client type. 
        If True, the broker will remove all information about this client when it disconnects. 
        If False, the client is a persistent client and subscription information 
        and queued messages will be retained when the client disconnects. 
        Note that a client will never discard its own outgoing messages on disconnect. 
        Calling connect() or reconnect() will cause the messages to be resent. 
        Use reinitialise() to reset a client to its original state. 
        The clean_session argument only applies to MQTT versions v3.1.1 and v3.1. 
        It is not accepted if the MQTT version is v5.0 - use the clean_start argument on connect() instead.
        
        userdata is user defined data of any type that is passed as the "userdata" parameter to callbacks. 
        It may be updated at a later point with the user_data_set() function.
        
        The protocol argument allows explicit setting of the MQTT version to use for this client. 
        Can be paho.mqtt.client.MQTTv311 (v3.1.1), paho.mqtt.client.MQTTv31 (v3.1) or 
        paho.mqtt.client.MQTTv5 (v5.0), with the default being v3.1.1.
        
        Set transport to "websockets" to use WebSockets as the transport mechanism. 
        Set to "tcp" to use raw TCP, which is the default.
        '''
        
        self.id = id
        self.client = mqtt.Client(client_id = client_id if not use_id_as_client_id else id,
                                  clean_session = clean_session,
                                  userdata = userdata,
                                  protocol = protocol,
                                  transport = transport,
                                  reconnect_on_failure = reconnect_on_failure)
        
        '''
        Following information must be passed before connecting to the broker.
        Use appropriate methods to do so.
        '''
        self.broker:str = "broker.hivemq.com"
        self.port:int = 1883
        self.pub_topic:str = None
        self.sub_topic:str = None
        
        '''
        Default subscription and publication callback
        '''
        self.sub_QoS = 0
        self.pub_QoS = 2    # Can be configured in the publish method
        
        '''
        use_on_message_callback_function is a boolean that determines
        whether an external function be used as a callback inside
        onMessage callback
        '''
        self.use_on_message_callback_function = False
        
        '''
        The callback function to be performed when onMessage
        callback function is called
        '''
        self.onMessageCallbackFunction = None
        
        '''
        Setting the callback functions
        '''
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        
        '''
        Message to publish on connection
        '''
        self.on_connect_msg = ""
        
        '''
        Whether to wait for publish status or not
        Keep in mind if it is set False (Default),
        then publish method might not return True
        even if it was published
        '''
        self.wait_for_publish_result = False
        
        '''
        wait_for_publish_timeout
        '''
        self.wait_for_publish_timeout = None
    
    def getID(self, id:str)->None:
        '''
        Get the ID of the device
        '''
        self.id = id
    
    def getOnConnectMessage(self, msg:str):
        '''
        Message to publish on connection
        '''
        self.on_connect_msg = msg
        
    def getMqttBroker(self, broker:str)->None:
        '''
        Get the MQTT broker url
        If it was changed while the client was connected,
        then the user must reconnect the client for the
        change to take place
        '''
        self.broker = broker
        
    def getMqttPort(self, port:int)->None:
        '''
        Get the MQTT port
        If it was changed while the client was connected,
        then the user must reconnect the client for the
        change to take place
        
        Keep in mind, if the port is associated with different 
        transport mechanism, then it will not work
        '''
        self.port = port
        
    def getMqttPubTopic(self, topic:str=None)->None:
        '''
        Get the default pub topic
        The client, if configured to send data periodically,
        then it will send data to this topic
        '''
        self.pub_topic = topic
        
    def getMqttSubTopic(self, topic:str=None)->None:
        '''
        Get the subscription topic.
        This code doesn't support multiple sub topics as of yet.
        
        The topic should be passed before calling connect,
        because subscription is done inside the callback
        function 'on_connect'
        '''
        self.sub_topic = topic
    
    def setDefaultSubQoS(self, qos:int)->None:
        '''
        Sets the default subscription QoS
        '''
        self.sub_QoS = qos
        
    def setDefaultPubQoS(self, qos:int)->None:
        '''
        Sets the default publication QoS
        '''
        self.pub_QoS = qos
        
    def setOnMessageCallbackFunction(self, func = None)->None:
        '''
        func is an externally defined function.
        This function will be called whenever onMessage is called.
        That is, when there's any incoming message in the MQTT broker's
        subscription topic
        
        The msg parameter of onMessage callback function will be passed into this
        function. 
        
        msg is an instance of MQTTMessage. 
        This is a class with members topic, payload, qos, retain.
        '''
        self.onMessageCallbackFunction = func
        if func is not None:
            self.use_on_message_callback_function = True
    
    def onConnect(self, client, userdata, flags, rc):
        '''
        Callback function for the mqtt client when it connects to the broker
        '''
        if len(self.on_connect_msg) != 0:
            self.client.publish(topic=self.pub_topic, payload= self.on_connect_msg)
        else:
            self.client.publish(topic=self.pub_topic, payload= self.id + ",connected")
        
        self.client.subscribe(self.sub_topic, qos=self.sub_QoS)
        
    
        
        
    def onMessage(self, client, userdata, msg):
        '''
        Callback function for the mqtt client when it there's any
        message in the sub topic
        '''
        # print(msg.topic+" "+str(msg.payload))
        
        if self.use_on_message_callback_function:
            self.onMessageCallbackFunction(msg)
    
    def setWaitForPublishResultTimeout(self, timeout:float=None, wait:bool=False):
        '''
        set wait_for_publish timeout
        Block until the message associated with this object is published, 
        or until the timeout occurs. 
        If timeout is None, this will never time out. 
        Set timeout to a positive number of seconds, e.g. 1.2, to enable the timeout.
        Raises ValueError if the message was not queued due to the outgoing queue being full.
        Raises RuntimeError if the message was not published for another reason.
        
        wait is a boolean that determines whether to use
        wait_for_publish or not
        '''
        self.wait_for_publish_timeout = timeout
        self.wait_for_publish_result = wait
        
    
    def publish(self, 
                payload = None, 
                topic: str = None,
                qos: int = None, 
                retain: bool = False, 
                properties = None)->bool:
        
        publish_result = self.client.publish(topic = topic if topic is not None else self.pub_topic, 
                                             payload = payload,
                                             qos = qos if qos is not None else self.pub_QoS, 
                                             retain = retain, 
                                             properties = properties)
        if self.wait_for_publish_result:
            publish_result.wait_for_publish(timeout=self.wait_for_publish_timeout)
        
        return publish_result.rc
    
    def connect(self,
                host:str = None, 
                port: int = None, 
                keepalive: int = None, 
                bind_address: str = None, 
                clean_start: int = None,
                properties = None) -> int:
        
        '''
        Connect to a remote broker.
        
        host is the hostname or IP address of the remote broker. 
        
        port is the network port of the server host to connect to. Defaults to 1883. 
        Note that the default port for MQTT over SSL/TLS is 8883 so if you are using tls_set() the port may need providing.
        
        keepalive: Maximum period in seconds between communications with the broker. 
        If no other messages are being exchanged, this controls the rate at which the 
        client will send ping messages to the broker.
        
        clean_start: (MQTT v5.0 only) True, False or MQTT_CLEAN_START_FIRST_ONLY. 
        Sets the MQTT v5.0 clean_start flag always, never or on the first successful connect only, respectively. 
        MQTT session data (such as outstanding messages and subscriptions) is cleared on successful 
        connect when the clean_start flag is set.
        
        properties: (MQTT v5.0 only) the MQTT v5.0 properties to be sent in the MQTT connect packet.
        '''
        
        self.client.connect(host = host if host is not None else self.broker, 
                            port = port if port is not None else self.port, 
                            keepalive = keepalive if keepalive is not None else 120, 
                            bind_address = bind_address if bind_address is not None else "",
                            # clean_start = clean_start,
                            properties = properties)
        # Todo
        # Solve the following
        # raise ValueError("Clean start only applies to MQTT V5")
        
        

if __name__ == "__main__":
    def execute(msg:mqtt.MQTTMessage):
        print(msg.payload.decode('utf-8').split())
        
    client = MqttClient(id="1111002301290000", use_id_as_client_id=False)
    client.getMqttSubTopic("dhrubo/mqtt/sub")
    client.getMqttPubTopic("dhrubo/mqtt/pub")
    client.setOnMessageCallbackFunction(execute)
    client.connect()
    client.client.loop_forever()
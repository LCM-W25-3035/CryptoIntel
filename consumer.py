{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "48ba7489-00b7-4cd8-bfb4-64793ae70598",
   "metadata": {},
   "outputs": [],
   "source": [
    "from confluent_kafka import Consumer\n",
    "import json\n",
    "\n",
    "# Kafka Config\n",
    "KAFKA_BROKER = \"localhost:9092\"\n",
    "TOPIC = \"crypto-events\"\n",
    "GROUP_ID = \"crypto-group\"\n",
    "\n",
    "# Create Consumer\n",
    "consumer = Consumer({\n",
    "    'bootstrap.servers': KAFKA_BROKER,\n",
    "    'group.id': GROUP_ID,\n",
    "    'auto.offset.reset': 'earliest'\n",
    "})\n",
    "\n",
    "consumer.subscribe([TOPIC])\n",
    "\n",
    "print(\"📥 Listening for crypto price updates...\")\n",
    "\n",
    "try:\n",
    "    while True:\n",
    "        msg = consumer.poll(1.0)  # Wait for message\n",
    "        if msg is None:\n",
    "            continue\n",
    "        if msg.error():\n",
    "            print(f\"❌ Error: {msg.error()}\")\n",
    "            continue\n",
    "        \n",
    "        data = json.loads(msg.value().decode('utf-8'))\n",
    "        print(f\"📩 Received: {data}\")\n",
    "\n",
    "except KeyboardInterrupt:\n",
    "    print(\"❌ Stopping consumer...\")\n",
    "finally:\n",
    "    consumer.close()\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

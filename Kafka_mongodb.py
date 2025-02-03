{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "f410eed6-9bd7-46d3-8ab3-482939b5778d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "MongoDB connected successfully!\n"
     ]
    }
   ],
   "source": [
    "from pymongo import MongoClient\n",
    "\n",
    "# Replace with your actual username, password, and cluster address\n",
    "client = MongoClient(\"mongodb+srv://crptointel:capstone@cluster0.00owi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0\", \n",
    "                     socketTimeoutMS=30000,  # Increase socket timeout to 30 seconds\n",
    "                     connectTimeoutMS=30000)  # Increase connection timeout to 30 seconds\n",
    "\n",
    "# Example: Test connection by pinging the server\n",
    "try:\n",
    "    client.admin.command('ping')\n",
    "    print(\"MongoDB connected successfully!\")\n",
    "except Exception as e:\n",
    "    print(\"MongoDB connection failed:\", e)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ea26b76d-95a3-4f71-be9c-dc3b041bf612",
   "metadata": {},
   "outputs": [],
   "source": []
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

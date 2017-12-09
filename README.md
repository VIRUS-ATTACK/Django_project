# Django_project
This project is about web GIS based IoT solutions for efficient water management of plants.
You can look the running website of this project at http://virusattack.pythonanywhere.com

Download the zip file(ITWS3-G23) and extract it, after extracting go to the ITWS3-G23 directory and open terminal in the current directory(ITWS3-G23) and run the command 'python manage.py runserver', it starts a development server at 'http://127.0.0.1:8000/' type this IP address in your local browser and you will go to our website.Please note that sensor directory contains two directories(reze,sens), sens directory contains a file named sensor.py which contains the code for collecting data from sensors and sending data to django website(Make sure that you have installed all the libraries i.e adafruit for DHT11 sensor,mcp 3008 module to read data from ADC,also make sure that you have all the sensors connected to the raspberry pi i.e temperature and humidity sensor DHT11,two soil moisture sensors,two 5V dc motors,one ultrasonic sensor HC SR-04,one water sensor or rain sensor) ,now run the code(sensor.py) with url  pointing to to the url of the Django website,for example if the url for the website is 'http://virusattack.pythonanywhere.com' then you must change the url in sensor.py code to url="http://virusattack.pythonanywhere.com/get/".


link to setup adafruit library for DHT11 sensor:https://medium.com/dyi-electronics/raspberry-pi-and-dht11-humidity-sensor-cccf6b3072ad

link to set mcp 3008 module to read values from adc:https://computers.tutsplus.com/tutorials/build-a-raspberry-pi-moisture-sensor-to-monitor-your-plants--mac-52875

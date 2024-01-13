# Electricity Data Stream

Project that creates a stream of electricity data. 

To start streaming localy, run the command: 

```
python -m app
```

# Virtual environment 

All the packages are in the requirements.txt file. To create a virtual environment with all the packages, run the command: 

```
python3.11 -m venv electricity-mock-env
```

To activate the virtual environment, run the command: 

```
# Bash
source electricity-mock-env/bin/activate

# Powershell
.\electricity-mock-env\Scripts\activate.ps1
```

# Container 

To create a container, run the command: 

```
docker build -t electricity-mock .
```

To run the container, run the command: 

```
docker run -p 8000:8000 electricity-mock
```

# Environment variables

All the environment variables are in the .env file. To run the application, you need to create a .env file with the following variables: 

```
# .env
EVENT_HUB_CONNECTION_STRING=Endpoint=
EVENT_HUB_NAME=
```

# Generating data stream 

To generate a data stream, run the command: 

```
python -m app
```

Go to `localhost:8000/stream_energy_data` to start generating the data stream. 
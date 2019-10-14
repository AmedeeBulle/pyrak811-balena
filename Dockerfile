# Start with the balenalib base image available on dockerhub
# -- The build version is required for GPIO access
# -- Python 3 is required for the rak811 package
FROM balenalib/raspberrypi3-debian-python:3-build

# Run the python package installer
# -- Installs the rak811 module/drivers
RUN pip install rak811

# Copy the application script
COPY pyrak811-balena.py /opt/rak811/

# Change the working directory
# -- Needed to run the script
WORKDIR /opt/rak811

# The entrypoint for the container
# -- Runs the script and exits if an error occurs
# -- Runs infinitely if no error is returned
CMD ["./pyrak811-balena.py"]


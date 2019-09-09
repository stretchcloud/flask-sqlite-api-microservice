FROM python:3.7-slim as python-base
WORKDIR /home/app

### Build the dependency libraries
FROM python-base as dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

### Build the layer
FROM dependencies as build

### Add user & group, copy over the program files & inject UUID to CSV
RUN addgroup --system app && adduser --system --ingroup app --no-create-home app
WORKDIR /home/app
RUN mkdir static
COPY apiapp.py .
COPY csv-insert.py .
COPY titanic.csv .
COPY data-import.sh .
COPY static/swagger.yml static/swagger.yml
RUN chmod +x data-import.sh
RUN python csv-insert.py

### Final Image build 
FROM python:3.7-alpine as release

### Install SQlite, copy the dependency libraries, import CSV to DB, change the ownership to user
WORKDIR /home/app
RUN apk add --update --no-cache sqlite
COPY --from=dependencies /home/app/requirements.txt .
COPY --from=dependencies /root/.cache /root/.cache
RUN pip install -r requirements.txt && rm -rf /root/.cache
COPY --from=build /home/app /home/app
COPY --from=build /etc/passwd /etc/passwd
COPY --from=build /etc/group /etc/group
RUN ./data-import.sh
RUN chown -R app:app ./
USER app

### Expose the flask app port and run the main app
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["apiapp.py"]
#######################################################
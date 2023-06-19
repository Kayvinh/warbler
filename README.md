# Warbler
Twitter clone - users can post/like messages and follow other users.

**Note: Please be patient, render is slow to load.**  
Deployed on: https://kevinnguyen-warbler.onrender.com/  
**Username: guest  
Password: password**  

## Local Setup

1. Navigate to `app/`. Create virtual environment and activate.

    ```
    cd app/  
    python3 -m venv venv  
    source venv/bin/activate
    ```

2. Install dependencies.

    ```
    pip3 install -r requirements.txt
    ```

3. Run app
    ```
    python3 -m flask run -p 5000
    ```


## TODO

- [ ] Incorporate instant messaging.
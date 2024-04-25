--! CTR + SHIFT + Q

-- cat helpers.sql | sqlite3 db.db
-- cat helpers.sql | sqlite3 db.db > output.txt
-- todo users table
-- CREATE TABLE users (
  -- id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
  -- username TEXT NOT NULL, 
  -- password_hash TEXT NOT NULL, 
  -- pomidors INTEGER NOT NULL DEFAULT 10,
  -- level INTEGER NOT NULL DEFAULT 0,
  -- experience INTEGER NOT NULL DEFAULT 0
  -- );

--todo usersTimeSettings table
-- CREATE TABLE usersTimeSettings (
--   users_id TEXT NOT NULL, 
--   workMins INTEGER NOT NULL DEFAULT 25,
--   workSecs INTEGER NOT NULL DEFAULT 0,
--   breakShortMins INTEGER NOT NULL DEFAULT 5,
--   breakShortSecs INTEGER NOT NULL DEFAULT 0,
--   breakLongMins INTEGER NOT NULL DEFAULT 15,
--   breakLongSecs INTEGER NOT NULL DEFAULT 0,
--   FOREIGN KEY(users_id) REFERENCES users(id)
--   );

-- --todo usersHistory
  -- CREATE TABLE usersHistory (
  -- users_id TEXT NOT NULL, 
  -- timestamp_info TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
  -- action_type TEXT CHECK(action_type IN ('reward', 'buy', 'train', 'unlock' )) NOT NULL,
  -- pomidors_number INTEGER NOT NULL,
  -- FOREIGN KEY(users_id) REFERENCES users(id)
  -- );

-- --todo usersComments
-- CREATE TABLE usersComments (
-- users_id TEXT NOT NULL, 
-- timestamp_info TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- comment TEXT NOT NULL,
-- FOREIGN KEY(users_id) REFERENCES users(id)
-- ); 

--todo usersMedals
-- CREATE TABLE usersMedals (
-- users_id TEXT NOT NULL, 
-- gold INTEGER NOT NULL DEFAULT 0,
-- silver INTEGER NOT NULL DEFAULT 0,
-- bronze INTEGER NOT NULL DEFAULT 0,
-- FOREIGN KEY(users_id) REFERENCES users(id)
-- ); 

--todo inserting/selecting/deleting
-- INSERT INTO usersTimeSettings (users_id, workMins, breakShortMins, breakLongMins)
-- VALUES ('Mis', 30, 3, 5)
-- VALUES ('Zefir', 15, 5, 10);


-- INSERT INTO users (username, password_hash)
-- VALUES ('Mis', '123');

-- SELECT * FROM users;

-- Deleting Data (one row)
    -- DELETE FROM users
    -- WHERE id >= 0;

-- SELECT * FROM usersComments;  

DELETE FROM users;
DELETE FROM usersTimeSettings;
DELETE FROM sqlite_sequence;
DELETE FROM usersComments;
DELETE FROM usersHistory;
DELETE FROM usersMedals;

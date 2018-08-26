import sqlite3
import os


class ConnectSQL:
    def __int__(self):
        self.path = None
        self.con = None
        self.cur = None

    def open(self):
        ConnectSQL.path = os.path.dirname(__file__) + "/w3.db"
        ConnectSQL.con = sqlite3.connect(ConnectSQL.path)
        ConnectSQL.cur = self.con.cursor()

    def sing_up(self, username, password, city):
        cur = self.con.cursor()
        cur.execute("insert into User (username, password,city) values (?,?,?)", (username, password, city))
        print("successfuly!")

    def check_city(self, city):
        hascity = 0
        cur = self.con.cursor()
        cur.execute("SELECT idc FROM city WHERE name = ? ", (city,))
        row = cur.fetchone()
        if row is not None:
            hascity = 1
        return hascity

    def write_to_city(self, name):
        sql = "INSERT INTO city(name) VALUES(?) "
        self.cur.execute(sql, (name,))

    def tran_city_to_id(self, city):
        sql = "SELECT idc FROM city WHERE name = ?"
        self.cur.execute(sql, (city,))
        row = self.cur.fetchone()
        return row[0]

    def check_sign_in(self, user, passw):
        sql = "SELECT * FROM  user WHERE username = ? and password = ?"
        self.cur.execute(sql, (user, passw))
        row = self.cur.fetchone()
        if row is None:
            return -1
        return row[0]

    def show_friend(self, id):
        print("-------List Friends-----------")
        sql = "SELECT user.username FROM friend left JOIN messenger on messenger.idrec = Friend.id2 " \
              "join user on user.id = Friend.id2 where id1 = ? AND isblock = 0 group by id2 order by messenger.time desc"
        self.cur.execute(sql, (id,))
        rows = self.cur.fetchall()
        for row in rows:
            print(row[0])

    def tran_name_to_id(self, frien):
        sql = "SELECT id FROM User WHERE username = ?"
        self.cur.execute(sql, (frien,))
        row = self.cur.fetchone()
        if row == None:
            return -1
        return row[0]

    def check_block(self, id1, id2):
        isblock = 0
        sql = "SELECT isblock FROM friend WHERE (id1 = ? AND id2 = ?) OR (id1 = ? AND id2 = ?)"
        self.cur.execute(sql, (id1, id2, id2, id1))
        row = self.cur.fetchone()
        if row is not None:
            isblock = 1
            return isblock
        return isblock

    def update_status_friend(self, status, id1, id2):
        who = 0
        if status == 1:
            who = id1
        sql = "UPDATE Friend SET RelationshipStatus = ? , whoblock = ? WHERE (id1 = ? AND id2 = ?) OR (id1 = ? AND id2 = ?)"
        self.cur.execute(sql, (status, who, id1, id2, id2, id1))

    def check_who_block(self, id1, id2):
        sql = "SELECT whoblock FROM Friend WHERE (id1 = ? AND id2 = ?) OR (id1 = ? AND id2 = ?)"
        self.cur.execute(sql, (id1, id2, id1, id2))
        row = self.cur.fetchone()
        whoblock = row[0]
        return whoblock

    def check_friend(self, id1, id2):
        Isfriend = 0
        sql = "SELECT * FROM friend WHERE ( id1 = ? AND id2 = ?) OR ( id1 = ? AND id2 = ?)"
        self.cur.execute(sql, (id1, id2, id2, id1))
        row = self.cur.fetchone()
        if row is not None:
            Isfriend = 1
            return Isfriend
        return Isfriend

    def write_to_friend(self, id1, id2):
        sql = "INSERT INTO friend VALUES (?,?,?,?),(?,?,?,?)"
        import time
        isblock = 0
        localtime = time.asctime(time.localtime(time.time()))
        self.cur.execute(sql, (id1, id2, isblock, localtime, id2, id1, isblock, localtime))
        self.con.commit()

    def tran_id_to_city(self, id1):
        sql = "SELECT name FROM city WHERE idc = ?"
        self.cur.execute(sql, (id1,))
        row = self.cur.fetchone()
        return row[0]

    def tran_id_user(self, id1):
        sql = "SELECT username FROM User WHERE id = ?"
        self.cur.execute(sql, (id1,))
        row = self.cur.fetchone()
        return row[0]

    def show_friend_by_city(self, id):
        sql = "SELECT city.idc,User.id FROM city, User,Friend WHERE (Friend.id1 = ? or Friend.id2 = ?) and (User.id = Friend.id1 or User.id = Friend.id2)  and User.city = city.idc and User.id != ?"
        self.cur.execute(sql, (id, id, id))
        row = self.cur.fetchone()
        city = dict()
        while row is not None:
            idc = row[0]
            idu = row[1]
            if city.get(row[0]) is None:
                city[idc] = [idu]
            else:
                city[idc].append(idu)
            row = self.cur.fetchone()
        for x in city:
            namecity = self.tran_id_to_city(x)
            print("City %s \n: ", namecity)
            print("Danh sach ban be: ")
            dem = 1;
            for y in city[x]:
                nameuser = self.tran_id_user(y)
                print(dem, ".", nameuser, "\n")
                dem = dem + 1
            print("\n\n")

    def write_mess(self, id1, id2, mess, time, status, sec):
        sql = "INSERT INTO messenger VALUES (?,?,?,?,?,?)"
        self.cur.execute(sql, (id1, id2, mess, time, status, sec))
        self.con.commit()

    def select_mess(self, id):
        sql = "SELECT DISTINCT user.username FROM" \
              "(SELECT * FROM messenger where idsen = ? ) as A LEFT JOIN user ON A.idrec = user.id"
        self.cur.execute(sql, (id,))
        row = self.cur.fetchone()
        print("Danh sach tin nhan: \n")
        dem = 1
        while row is not None:
            print(dem, ".", row[0])
            dem += 1
            row = self.cur.fetchone()

    def show_mess_detail(self, id1, id2):
        print("---------Detail-----\n")
        sql = "SELECT User.username, B.contend, B.time FROM (SELECT * FROM messenger WHERE (idsen = ? OR idsen = ?) AND (idrec = ? OR idrec =?) ) AS B LEFT JOIN  user ON user.id = B.idsen"
        self.cur.execute(sql, (id1, id2, id1, id2))
        row = self.cur.fetchone()
        while row is not None:
            print(row[0], ":")
            print(row[1], "-", row[2])
            row = self.cur.fetchone()

    def block(self, id1, id2):
        sql = "UPDATE friend SET isblock = 1 WHERE id1 = ? AND id2 = ?"
        self.cur.execute(sql, (id1, id2))
        self.con.commit()

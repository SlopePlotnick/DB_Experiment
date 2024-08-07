import psycopg2
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
import tkinter.messagebox as messagebox  # 弹窗
# 打包的时候会用到（十进制的一个库）
import decimal

decimal.__version__

class StartPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁上一个窗口
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('商品信息管理系统')
        self.window.geometry('300x410+500+100')  # 这里的乘是小x，第一个参数表示窗口的长，第二个表示宽，第三个表示的距离屏幕左边界的距离，第三个为距离上边界的距离

        label = Label(self.window, text="商品信息管理系统", font=("Verdana", 20))
        label.pack(pady=100)  # pady=100 这个label距离窗口上边界的距离，这里设置为100刚好居中

        # command=lambda:  可以带参数，注意带参数的类不要写括号，否者，这里调用会直接执行(class test:)
        Button(self.window, text="用户登陆", font=tkFont.Font(size=16), command=lambda: LoginPage(self.window),
               width=30, height=2,
               fg='black', bg='gray', activebackground='black',
               activeforeground='white').pack()  # pack() 方法会使得组件在窗口中自动布局
        Button(self.window, text="数据库初始化", font=tkFont.Font(size=16), command=self.initialization, width=30,
               height=2,
               fg='black', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="退出系统", height=2, font=tkFont.Font(size=16), width=30, command=self.window.destroy,
               fg='black', bg='gray', activebackground='black', activeforeground='white').pack()

        self.window.mainloop()  # 主消息循环

    # 创建数据表
    def initialization(self):
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33",
                              port=26000)  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()
        print('建立数据表中......')
        sql = """
		---创建用户数据表
		CREATE TABLE t_user (
		id varchar(255) NOT NULL,
		passwd varchar(255) NOT NULL,
		name varchar(255) DEFAULT NULL,
		number varchar(11) DEFAULT NULL,
		addr varchar(255) DEFAULT NULL,
		type varchar(2) NOT NULL, ---0表示管理员 1表示普通用户
		PRIMARY KEY (id)
		);


		---创建商品表
		CREATE TABLE t_goods (
		id varchar(20) NOT NULL,
		name varchar(20) DEFAULT NULL,
		price int NOT NULL CHECK ( price >= 0 ), ---实际上用来表示库存量
		PRIMARY KEY (id)
		);

		---创建订单信息表
		CREATE TABLE t_order(
		id varchar(20) NOT NULL,
		gid varchar(20) NOT NULL,
		uid varchar(255) NOT NULL,
		buy_time varchar(255) DEFAULT NULL,
		money int NOT NULL, ---实际上用来表示订单量
		PRIMARY KEY (id),
		FOREIGN KEY (gid) REFERENCES t_goods(id),
		FOREIGN KEY (uid) REFERENCES t_user(id)
		);

        CREATE INDEX t_order_uid ON t_order USING HASH (uid);
		"""

        try:
            cursor.execute(sql)
            db.commit()
        except:
            messagebox.showinfo('警告！', '数据创建失败')
        cursor.close()  # 关闭游标
        db.close()  # 关闭数据库连接
        self.create_trigger1()

    def create_trigger1(self):
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33",
                              port=26000)  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()
        print('建立触发器中......')
        sql = """
        CREATE OR REPLACE FUNCTION func_insert()
        RETURNS TRIGGER
        LANGUAGE PLPGSQL
        AS
        $$
        BEGIN
          IF TG_OP = 'INSERT' THEN
            UPDATE t_goods set price = (price - NEW.money) WHERE id = new.gid;
            RETURN NEW;
          END IF;
          RETURN NEW;
        END;
        $$;

        CREATE TRIGGER trigger_insert
        AFTER INSERT ON t_order
        FOR EACH ROW
        EXECUTE PROCEDURE func_insert();
        """

        try:
            cursor.execute(sql)
            db.commit()
        except:
            messagebox.showinfo('警告！', '触发器创建失败')
        cursor.close()  # 关闭游标
        db.close()  # 关闭数据库连接
        self.create_trigger2()  # 创建触发器1

    def create_trigger2(self):
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33",
                              port=26000)  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()
        print('建立触发器中......')
        sql = """
        CREATE OR REPLACE FUNCTION func_delete_trigger()
        RETURNS TRIGGER
        LANGUAGE PLPGSQL
        AS
        $$
        BEGIN
          IF TG_OP = 'DELETE' THEN
            UPDATE t_goods set price = (price + OLD.money) WHERE id = OLD.gid;
            RETURN OLD;
          END IF;
          RETURN OLD;
        END;
        $$;

        CREATE TRIGGER trigger_delete
        AFTER DELETE ON t_order
        FOR EACH ROW
        EXECUTE PROCEDURE func_delete_trigger();
        """
        try:
            cursor.execute(sql)
            db.commit()
        except:
            messagebox.showinfo('警告！', '触发器创建失败')
        cursor.close()  # 关闭游标
        db.close()  # 关闭数据库连接
        self.create_trigger3()  # 创建触发器1

    def create_trigger3(self):
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33",
                              port=26000)  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()
        print('建立触发器中......')
        sql = """
        CREATE OR REPLACE FUNCTION func_update()
        RETURNS TRIGGER
        LANGUAGE PLPGSQL
        AS
        $$
        BEGIN
          IF TG_OP = 'UPDATE' THEN
            UPDATE t_goods set price = (price + OLD.money) WHERE id = OLD.gid;
            UPDATE t_goods set price = (price - NEW.money) WHERE id = NEW.gid;
            RETURN OLD;
          END IF;
          RETURN OLD;
        END;
        $$;

        CREATE TRIGGER trigger_update
        AFTER UPDATE ON t_order
        FOR EACH ROW
        EXECUTE PROCEDURE func_update();
        """
        try:
            cursor.execute(sql)
            db.commit()
        except:
            messagebox.showinfo('警告！', '触发器创建失败')
        cursor.close()  # 关闭游标
        db.close()  # 关闭数据库连接
        self.create_function1()  # 创建触发器1


    # 创建存储过程1
    def create_function1(self):
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33",
                              port=26000)  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()
        print('建立存储过程1中......')
        sql = """
		-- 创建删除指定行的存储过程
		CREATE OR REPLACE FUNCTION func_delete(p_商品id VARCHAR(20)) 
		RETURNS VOID AS 
		$$
		BEGIN
			DELETE FROM t_goods WHERE id = p_商品id;
		END;
		$$
		LANGUAGE 'plpgsql';
		"""

        try:
            cursor.execute(sql)
            db.commit()
        except:
            messagebox.showinfo('警告！', '过程1创建失败')
        cursor.close()  # 关闭游标
        db.close()  # 关闭数据库连接
        self.create_function2()

    # 创建存储过程2
    def create_function2(self):
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33",
                              port=26000)  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()
        print('建立存储过程2中......')
        sql = """
		-- 创建查询的存储过程
		CREATE OR REPLACE FUNCTION proc_cha(p_name varchar)
		RETURNS TABLE(
            id varchar(20),
            name varchar(20),
            price int
		)
		LANGUAGE plpgsql
		AS $$
		BEGIN
			return query SELECT * FROM t_goods WHERE name = p_name;
		END;
		$$;
		"""

        try:
            cursor.execute(sql)
            db.commit()
            messagebox.showinfo('提示', '数据库已成功初始化')
        except:
            messagebox.showinfo('警告！', '过程2创建失败')
        cursor.close()  # 关闭游标
        db.close()  # 关闭数据库连接

# 管理员登陆页面
class LoginPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('用户登陆页面')
        self.window.geometry('450x300+500+100')

        # 创建画布，这里可以存放照片等组件
        canvas = tk.Canvas(self.window, height=200, width=500)
        image_file = tk.PhotoImage(file='welcome.gif')
        image = canvas.create_image(0, 0, anchor='nw', image=image_file)  # 前两个参数为画布得坐标，anchor=nw则是把图片的左上角作为锚定点
        canvas.pack(side='top')  # 使用pack将画布进行简单得布局，放到了上半部分

        # 创建提示信息
        tk.Label(self.window, text='登录名: ').place(x=80, y=150)
        tk.Label(self.window, text='登陆密码: ').place(x=80, y=190)

        self.login_username = tk.Entry(self.window)
        self.login_username.place(x=160, y=150)
        self.login_pass = tk.Entry(self.window, show='*')
        self.login_pass.place(x=160, y=190)
        # 登陆和返回首页得按钮
        btn_login = tk.Button(self.window, text='登陆', width=10, command=self.login)
        btn_login.place(x=120, y=230)
        btn_back = Button(self.window, text="返回首页", width=8, font=tkFont.Font(size=12), command=self.back)
        btn_back.place(x=270, y=230)
        self.window.mainloop()

    # 登陆的函数
    def login(self):
        # 数据库操作 查询管理员表
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33",
                              port=26000)  # 服务器名,账户,密码,数据库名
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_user where id = '%s'" % (
            self.login_username.get())  # 这里得user_name即为id，这里是输入的用户名
        login_id = None
        login_pass = None
        login_type = None
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表，这里是返回的二元元组，如(('id','title'),('id','title'))
            results = cursor.fetchall()
            for row in results:
                login_id = row[0]
                login_pass = row[1]
                login_type = row[5]
                # 打印结果
                print("登陆账号为：%s\n登陆密码为：%s\n用户身份为：%s" % (login_id, login_pass, login_type))
        except:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '无法获取用户数据 请检查网络')
        db.close()  # 关闭数据库连接

        print("正在登陆用户.......")

        # 判断输入的账号密码与数据库中的信息是否一致a
        if self.login_pass.get() == login_pass:
            if login_type == '0':
                print('管理员用户登陆成功')
                AdminMenu(self.window)  # 进入管理员子菜单操作界面
            else:
                print('普通用户登陆成功')
                UserMenu(self.window, login_id)
        else:
            messagebox.showinfo('警告！', '用户名或密码不正确！')

    # 使得系统点击关闭的x号上返回指定页面，而不是关闭
    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口

# 管理员子菜单操作界面
class AdminMenu:
    def __init__(self, parent_window):
        parent_window.destroy()  # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('信息管理界面')
        self.window.geometry('300x410+500+100')
        label = Label(self.window, text="请选择需要进行的操作", font=("Verdana", 20))
        label.pack(pady=100)  # pady=100 界面的长度

        Button(self.window, text="商品信息管理", font=tkFont.Font(size=16), width=30, height=2,
               command=lambda: AdminGoods(self.window),
               fg='black', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="买家信息管理", font=tkFont.Font(size=16), width=30, height=2,
               command=lambda: AdminUser(self.window),
               fg='black', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="订单信息管理", font=tkFont.Font(size=16), width=30, height=2,
               command=lambda: AdminOrder(self.window),
               fg='black', bg='gray', activebackground='black', activeforeground='white').pack()

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口

# 商品信息操作界面
class AdminGoods:
    def __init__(self, parent_window):
        parent_window.destroy()  # 自动销毁上一个界面
        self.window = Tk()  # 初始框的声明
        self.window.title('管理员操作界面')
        self.window.geometry("650x685+300+30")  # 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=300, height=200)  # 指定框架，在窗口上可以显示，这里指定四个框架
        self.frame_right_top = tk.Frame(width=200, height=200)
        self.frame_center = tk.Frame(width=500, height=350)
        self.frame_bottom = tk.Frame(width=650, height=70)

        # 定义下方中心列表区域
        self.columns = ("商品id", "商品名称", "库存量")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 定义id1为修改id时的暂存变量，这个是为了更新信息而设计的
        self.id1 = 0

        # 表格的标题
        self.tree.column("商品id", width=int(500/3), anchor='center')
        self.tree.column("商品名称", width=int(500/3), anchor='center')
        self.tree.column("库存量", width=int(500/3), anchor='center')

        # grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        # 定义几个数组，为中间的那个大表格做一些准备
        self.id = []
        self.name = []
        self.price = []

        # 打开数据库连接
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_goods"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.name.append(row[1])
                self.price.append(row[2])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        print("test***********************")
        for i in range(min(len(self.id), len(self.name), len(self.price))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.name[i], self.price[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="商品信息:", font=('Verdana', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)  # NSEW表示允许组件向4个方向都可以拉伸

        # 定义下方区域
        self.chaxun = StringVar()
        self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_id = StringVar()  # 声明学号
        self.var_name = StringVar()  # 声明姓名
        self.var_price = StringVar()  # 声明性别
        # 商品id
        self.right_top_id_label = Label(self.frame_left_top, text="商品id： ", font=('Verdana', 15))
        self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 15))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
        # 商品名称
        self.right_top_name_label = Label(self.frame_left_top, text="商品名称：", font=('Verdana', 15))
        self.right_top_name_entry = Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 15))
        self.right_top_name_label.grid(row=2, column=0)  # 位置设置
        self.right_top_name_entry.grid(row=2, column=1)
        # 库存量
        self.right_top_gender_label = Label(self.frame_left_top, text="库存量：", font=('Verdana', 15))
        self.right_top_gender_entry = Entry(self.frame_left_top, textvariable=self.var_price, font=('Verdana', 15))
        self.right_top_gender_label.grid(row=3, column=0)  # 位置设置
        self.right_top_gender_entry.grid(row=3, column=1)

        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 20))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建商品信息', width=15, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中商品信息', width=15,
                                            command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中商品信息', width=15,
                                            command=self.del_row)

        # 定义下方区域，查询功能块
        self.chaxun = StringVar()
        self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)

        # 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)

        # 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        # 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

    # 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()  # 先将表格内的内容全部清空

        # print(self.chaxun.get())	# 输入框内的内容
        # 打开数据库连接，准备查找指定的信息
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM proc_cha('%s');" % (self.chaxun.get())
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            # 再次进行初始化，进行首行数据的插入
            self.id = []
            self.name = []
            self.price = []
            # 向表格中插入数据
            for row in results:
                self.id.append(row[0])
                self.name.append(row[1])
                self.price.append(row[2])

        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
            return
            db.close()  # 关闭数据库连接

        print("进行数据的插入")
        for i in range(min(len(self.id), len(self.name), len(self.price))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.name[i], self.price[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    # 清空表格中的所有信息
    def delButton(self):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

    # 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
        self.id1 = self.var_id.get()
        self.var_name.set(self.row_info[1])
        self.var_price.set(self.row_info[2])
        self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id,
                                        font=('Verdana', 15))

    # 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def new_row(self):
        print('123')
        print(self.var_id.get())
        print(self.id)
        if str(self.var_id.get()) in self.id:
            messagebox.showinfo('警告！', '该商品已存在！')
        else:
            if self.var_id.get() != '' and self.var_name.get() != '' and self.var_price.get() != '':
                # 打开数据库连接
                db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33",
                                      port=26000)
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "INSERT INTO t_goods(id, name, price) \
				       VALUES ('%s', '%s', '%s')" % \
                      (self.var_id.get(), self.var_name.get(), self.var_price.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    return
                db.close()  # 关闭数据库连接

                self.id.append(self.var_id.get())
                self.name.append(self.var_name.get())
                self.price.append(self.var_price.get())
                self.tree.insert('', len(self.id) - 1, values=(
                    self.id[len(self.id) - 1], self.name[len(self.id) - 1], self.price[len(self.id) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写商品信息')

    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
            # 打开数据库连接
            db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "UPDATE t_goods SET id = '%s', name = '%s', price = '%s'where id = '%s'" % (
            self.var_id.get(), self.var_name.get(), self.var_price.get(), self.id1)  # SQL 插入语句
            print(self.var_id.get())
            print(self.var_name.get())
            print(self.var_price.get())
            print(self.id1)
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
                return
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            self.name[id_index] = self.var_name.get()
            self.price[id_index] = self.var_price.get()

            self.tree.item(self.tree.selection()[0], values=(
                self.var_id.get(), self.var_name.get(), self.var_price.get()))  # 修改对于行信息

    # 删除行
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的学号
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
            # 打开数据库连接
            db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql ="""
            DELETE FROM t_order WHERE gid = '%s';
            SELECT func_delete('%s');
            """ % (self.row_info[0], self.row_info[0])  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
                return
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            print(id_index)
            del self.id[id_index]
            del self.name[id_index]
            del self.price[id_index]
            print(self.id)
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())

    def back(self):
        AdminMenu(self.window)  # 进入管理员子菜单操作界面

# 买家信息操作界面
class AdminUser:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        self.window = Tk()  # 初始框的声明
        self.window.title('管理员操作界面')
        self.window.geometry("1000x685+300+30")  # 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=600, height=250)
        self.frame_right_top = tk.Frame(width=400, height=200)
        self.frame_center = tk.Frame(width=800, height=350)
        self.frame_bottom = tk.Frame(width=500, height=70)

        self.id1 = 0

        # 定义下方中心列表区域
        self.columns = ("用户id", "用户密码", "姓名", "电话", "地址", "用户类型")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("用户id", width=150, anchor='center')  # 表示列,不显示
        self.tree.column("用户密码", width=150, anchor='center')
        self.tree.column("姓名", width=100, anchor='center')
        self.tree.column("电话", width=100, anchor='center')
        self.tree.column("地址", width=200, anchor='center')
        self.tree.column("用户类型", width=100, anchor='center')

        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.id = []
        self.passwd = []
        self.name = []
        self.number = []
        self.addr = []
        self.type = []
        # 打开数据库连接
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_user"  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.passwd.append(row[1])
                self.name.append(row[2])
                self.number.append(row[3])
                self.addr.append(row[4])
                self.type.append(row[5])
        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        print("test***********************")
        for i in range(min(len(self.id), len(self.passwd), len(self.name), len(self.number), len(self.addr), len(self.type))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.passwd[i], self.name[i], self.number[i], self.addr[i], self.type[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="用户信息:", font=('Verdana', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=200, pady=10)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_id = StringVar()  # 声明学号
        self.var_passwd = StringVar()
        self.var_name = StringVar()  # 声明姓名
        self.var_number = StringVar()
        self.var_addr = StringVar()
        self.var_type = StringVar()
        # id
        self.right_top_id_label = Label(self.frame_left_top, text="用户id：", font=('Verdana', 15))
        self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 15))
        self.right_top_id_label.grid(row=1, column=0, padx=100)  # 位置设置
        self.right_top_id_entry.grid(row=1, column=1)
        # passwd
        self.right_top_passwd_label = Label(self.frame_left_top, text="用户密码：", font=('Verdana', 15))
        self.right_top_passwd_entry = Entry(self.frame_left_top, textvariable=self.var_passwd, font=('Verdana', 15))
        self.right_top_passwd_label.grid(row=2, column=0)  # 位置设置
        self.right_top_passwd_entry.grid(row=2, column=1)
        # name
        self.right_top_name_label = Label(self.frame_left_top, text="姓名：", font=('Verdana', 15))
        self.right_top_name_entry = Entry(self.frame_left_top, textvariable=self.var_name,
                                            font=('Verdana', 15))
        self.right_top_name_label.grid(row=3, column=0)  # 位置设置
        self.right_top_name_entry.grid(row=3, column=1)
        # number
        self.right_top_number_label = Label(self.frame_left_top, text="电话：", font=('Verdana', 15))
        self.right_top_number_entry = Entry(self.frame_left_top, textvariable=self.var_number,
                                            font=('Verdana', 15))
        self.right_top_number_label.grid(row=4, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=4, column=1)
        # addr
        self.right_top_addr_label = Label(self.frame_left_top, text="地址：", font=('Verdana', 15))
        self.right_top_addr_entry = Entry(self.frame_left_top, textvariable=self.var_addr,
                                            font=('Verdana', 15))
        self.right_top_addr_label.grid(row=5, column=0)  # 位置设置
        self.right_top_addr_entry.grid(row=5, column=1)
        # type
        self.right_top_type_label = Label(self.frame_left_top, text="类型：", font=('Verdana', 15))
        self.right_top_type_entry = Entry(self.frame_left_top, textvariable=self.var_type,
                                            font=('Verdana', 15))
        self.right_top_type_label.grid(row=6, column=0)  # 位置设置
        self.right_top_type_entry.grid(row=6, column=1)

        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 20))

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建用户信息', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中用户信息', width=20,
                                            command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中用户信息', width=20,
                                            command=self.del_row)

        # 定义下方区域
        self.chaxun = StringVar()
        self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='买家姓名查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)

        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=0, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    # 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()  # 先将表格内的内容全部清空

        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_user where NAME = '%s'" % (self.chaxun.get())
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            # 再次进行初始化，进行首行数据的插入
            self.id = []
            self.passwd = []
            self.name = []
            self.number = []
            self.addr = []
            self.type = []
            # 向表格中插入数据
            for row in results:
                self.id.append(row[0])
                self.passwd.append(row[1])
                self.name.append(row[2])
                self.number.append(row[3])
                self.addr.append(row[4])
                self.type.append(row[5])

        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
            return
            db.close()  # 关闭数据库连接

        print("进行数据的插入")
        for i in range(min(len(self.id), len(self.passwd), len(self.name), len(self.number), len(self.addr), len(self.type))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.passwd[i], self.name[i], self.number[i], self.addr[i], self.type[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    # 清空表格中的所有信息
    def delButton(self):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

    def back(self):
        AdminMenu(self.window)  # 进入管理员子菜单操作界面

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
        self.id1 = self.var_id.get()
        print(self.id1)
        self.var_passwd.set(self.row_info[1])
        self.var_name.set(self.row_info[2])
        self.var_number.set(self.row_info[3])
        self.var_addr.set(self.row_info[4])
        self.var_type.set(self.row_info[5])
        self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id,
                                        font=('Verdana', 15))

    # 排序的方法
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    # 插入方法
    def new_row(self):
        if str(self.var_id.get()) in self.id:
            messagebox.showinfo('警告！', '该用户已存在！')
        else:
            if self.var_id.get() != '' and self.var_passwd.get() != '' and self.var_name.get() != '' and self.var_number.get() != '' and self.var_addr.get() != '' and self.var_type.get() != '':
                # 打开数据库连接
                db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33",
                                      port=26000)
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "INSERT INTO t_user(id, passwd, name, number, addr, type) \
				       VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
                      (self.var_id.get(), self.var_passwd.get(), self.var_name.get(), self.var_number.get(), self.var_addr.get(), self.var_type.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    return
                db.close()  # 关闭数据库连接

                # 将信息写入到表格中
                self.id.append(self.var_id.get())
                self.passwd.append(self.var_passwd.get())
                self.name.append(self.var_name.get())
                self.number.append(self.var_number.get())
                self.addr.append(self.var_addr.get())
                self.type.append(self.var_type.get())
                self.tree.insert('', len(self.id) - 1, values=(
                self.id[len(self.id) - 1], self.passwd[len(self.id) - 1], self.name[len(self.id) - 1], self.number[len(self.id) - 1], self.addr[len(self.id) - 1], self.type[len(self.id) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写商品信息')

    # 更新数据及表格
    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
            # 打开数据库连接
            db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "UPDATE t_user SET id = '%s', passwd = '%s', name = '%s', number = '%s', addr = '%s', type = '%s' \
				where id = '%s'" % (
            self.var_id.get(), self.var_passwd.get(), self.var_name.get(), self.var_number.get(), self.var_addr.get(), self.var_type.get(), self.id1)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
                return
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            self.passwd[id_index] = self.var_passwd.get()
            self.name[id_index] = self.var_name.get()
            self.number[id_index] = self.var_number.get()
            self.addr[id_index] = self.var_addr.get()
            self.type[id_index] = self.var_type.get()

            self.tree.item(self.tree.selection()[0], values=(
                self.var_id.get(), self.var_passwd.get(), self.var_name.get(), self.var_number.get(), self.var_addr.get(), self.var_type.get()))  # 修改对于行信息

    # 删除行
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的学号
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
            # 打开数据库连接
            db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "DELETE FROM t_user WHERE id = '%s'" % (self.row_info[0])  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
                return
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            print(id_index)
            del self.id[id_index]
            del self.passwd[id_index]
            del self.name[id_index]
            del self.number[id_index]
            del self.addr[id_index]
            del self.type[id_index]
            print(self.id)
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())

# 订单信息操作界面
class AdminOrder:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        self.window = Tk()  # 初始框的声明
        self.window.geometry("650x750+300+30")  # 初始窗口在屏幕中的位置
        self.window.title('管理员操作界面')

        self.frame_left_top = tk.Frame(width=300, height=230)
        self.frame_right_top = tk.Frame(width=200, height=230)
        self.frame_center = tk.Frame(width=500, height=360)
        self.frame_bottom = tk.Frame(width=650, height=60)

        self.id1 = 0

        # 定义下方中心列表区域
        self.columns = ("订单id", "商品id", "用户id", "订单创建时间", "订单量")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("订单id", width=100, anchor='center')  # 表示列,不显示
        self.tree.column("商品id", width=100, anchor='center')
        self.tree.column("用户id", width=100, anchor='center')
        self.tree.column("订单创建时间", width=100, anchor='center')
        self.tree.column("订单量", width=100, anchor='center')

        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.id = []
        self.gid = []
        self.uid = []
        self.buy_time = []
        self.money = []
        self.page = 0  # 初始化页数
        self.limit = 500  # 数据量限制
        # 打开数据库连接
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_order LIMIT 500"  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.gid.append(row[1])
                self.uid.append(row[2])
                self.buy_time.append(row[3])
                self.money.append(row[4])
        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        print("test***********************")
        for i in range(min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="订单信息:", font=('Verdana', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_id = StringVar()  # 声明商品id
        self.var_gid = StringVar()  # 声明订单id
        self.var_uid = StringVar()  # 声明订单创建时间
        self.var_buy_time = StringVar()  # 声明订单是否成功交易
        self.var_money = StringVar()  # 声明交易金额

        self.right_top_id_label = Label(self.frame_left_top, text="订单id:", font=('Verdana', 15))
        self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 15))
        self.right_top_id_label.grid(row=1, column=0)  # 位置设置
        self.right_top_id_entry.grid(row=1, column=1)

        self.right_top_gid_label = Label(self.frame_left_top, text="商品id:", font=('Verdana', 15))
        self.right_top_gid_entry = Entry(self.frame_left_top, textvariable=self.var_gid, font=('Verdana', 15))
        self.right_top_gid_label.grid(row=2, column=0)  # 位置设置
        self.right_top_gid_entry.grid(row=2, column=1)

        self.right_top_uid_label = Label(self.frame_left_top, text="用户id:", font=('Verdana', 15))
        self.right_top_uid_entry = Entry(self.frame_left_top, textvariable=self.var_uid, font=('Verdana', 15))
        self.right_top_uid_label.grid(row=3, column=0)  # 位置设置
        self.right_top_uid_entry.grid(row=3, column=1)

        self.right_top_buy_time_label = Label(self.frame_left_top, text="创建时间:", font=('Verdana', 15))
        self.right_top_buy_time_entry = Entry(self.frame_left_top, textvariable=self.var_buy_time, font=('Verdana', 15))
        self.right_top_buy_time_label.grid(row=4, column=0)  # 位置设置
        self.right_top_buy_time_entry.grid(row=4, column=1)

        self.right_top_money_label = Label(self.frame_left_top, text="订单量:", font=('Verdana', 15))
        self.right_top_money_entry = Entry(self.frame_left_top, textvariable=self.var_money, font=('Verdana', 15))
        self.right_top_money_label.grid(row=5, column=0)  # 位置设置
        self.right_top_money_entry.grid(row=5, column=1)

        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 20))

        self.tree.bind('<Button-1>', self.info)  # 左键获取位置
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建订单信息', width=15, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中订单信息', width=15,
                                            command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中订单信息', width=15,
                                            command=self.del_row)
        self.right_top_button4 = ttk.Button(self.frame_right_top, text='查询', width=15,
                                            command=self.put_data)

        # 定义下方区域
        # 设置第一页和最后一页按钮
        self.first_button = ttk.Button(self.frame_bottom, text='第一页', command=self.first_page)
        self.last_button = ttk.Button(self.frame_bottom, text='最后一页', command=self.last_page)
        self.first_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.last_button.grid(row=0, column=3, padx=20, pady=20)  # 位置设置
        # 设置下页和上页按钮
        self.next_button = ttk.Button(self.frame_bottom, text='下一页', command=self.next_page)
        self.previous_button = ttk.Button(self.frame_bottom, text='上一页', command=self.previous_page)
        self.next_button.grid(row=0, column=1, padx=20, pady=20)  # 位置设置
        self.previous_button.grid(row=0, column=2, padx=20, pady=20)  # 位置设置
        # 设置重置按钮
        self.reset_button = ttk.Button(self.frame_bottom, text='重置', command=self.first_page)
        self.reset_button.grid(row=0, column=4, padx=20, pady=20)  # 位置设置

        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
        self.right_top_button4.grid(row=5, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        AdminMenu(self.window)  # 进入管理员子菜单操作界面

        # 定义查找数据的方法

    def info(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
        self.id1 = self.var_id.get()
        print(self.id1)
        self.var_gid.set(self.row_info[1])
        self.var_uid.set(self.row_info[2])
        self.var_buy_time.set(self.row_info[3])
        self.var_money.set(self.row_info[4])

        var_uname = StringVar()
        var_gname = StringVar()

        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = """
        SELECT t_user.name, t_goods.name
        FROM t_user, t_goods
        WHERE t_user.id = '%s' AND t_goods.id = '%s'
        """ % (self.var_uid.get(), self.var_gid.get()) # SQL 插入语句
        try:
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            for row in results:
                var_uname.set(row[0])
                var_gname.set(row[1])
        except:
            db.rollback()  # 发生错误时回滚
            messagebox.showinfo('警告！', '查询失败，数据库连接失败！')
            return
        db.close()  # 关闭数据库连接

        newwindow = Toplevel()  # 初始框的声明
        newwindow.grab_set()
        newwindow.focus()
        newwindow.title('详情')
        newwindow.geometry("600x300+300+200")  # 初始窗口在屏幕中的位置

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(newwindow, text="订单信息:", font=('Verdana', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=200, pady=10)
        # id
        self.right_top_id_label = Label(newwindow, text="订单id：", font=('Verdana', 15))
        self.right_top_id_entry = Entry(newwindow, textvariable=self.var_id, font=('Verdana', 15),
                                        state=DISABLED)
        self.right_top_id_label.grid(row=1, column=0, padx=100)  # 位置设置
        self.right_top_id_entry.grid(row=1, column=1)
        # gid
        self.right_top_gid_label = Label(newwindow, text="商品id：", font=('Verdana', 15))
        self.right_top_gid_entry = Entry(newwindow, textvariable=self.var_gid, font=('Verdana', 15), state=DISABLED)
        self.right_top_gid_label.grid(row=2, column=0)  # 位置设置
        self.right_top_gid_entry.grid(row=2, column=1)
        # gname
        self.right_top_gname_label = Label(newwindow, text="商品名称：", font=('Verdana', 15))
        self.right_top_gname_entry = Entry(newwindow, textvariable=var_gname, font=('Verdana', 15), state=DISABLED)
        self.right_top_gname_label.grid(row=3, column=0)  # 位置设置
        self.right_top_gname_entry.grid(row=3, column=1)
        # uid
        self.right_top_uid_label = Label(newwindow, text="用户id：", font=('Verdana', 15))
        self.right_top_uid_entry = Entry(newwindow, textvariable=self.var_uid,
                                          font=('Verdana', 15), state=DISABLED)
        self.right_top_uid_label.grid(row=4, column=0)  # 位置设置
        self.right_top_uid_entry.grid(row=4, column=1)
        # uname
        self.right_top_uname_label = Label(newwindow, text="用户姓名：", font=('Verdana', 15))
        self.right_top_uname_entry = Entry(newwindow, textvariable=var_uname,
                                          font=('Verdana', 15), state=DISABLED)
        self.right_top_uname_label.grid(row=5, column=0)  # 位置设置
        self.right_top_uname_entry.grid(row=5, column=1)
        # buy_time
        self.right_top_buy_time_label = Label(newwindow, text="创建时间：", font=('Verdana', 15))
        self.right_top_buy_time_entry = Entry(newwindow, textvariable=self.var_buy_time,
                                            font=('Verdana', 15), state=DISABLED)
        self.right_top_buy_time_label.grid(row=6, column=0)  # 位置设置
        self.right_top_buy_time_entry.grid(row=6, column=1)
        # money
        self.right_top_money_label = Label(newwindow, text="订单量：", font=('Verdana', 15))
        self.right_top_money_entry = Entry(newwindow, textvariable=self.var_money,
                                          font=('Verdana', 15), state=DISABLED)
        self.right_top_money_label.grid(row=7, column=0)  # 位置设置
        self.right_top_money_entry.grid(row=7, column=1)


        # 整体区域定位
        newwindow.grid(row=0, column=0, padx=2, pady=5)

        newwindow.grid_propagate(0)

        newwindow.tkraise()  # 开始显示主菜单

    def search_data(self):
        # 打开数据库连接
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = f"SELECT * FROM t_order LIMIT {self.limit} OFFSET {self.page * self.limit}"  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.gid.append(row[1])
                self.uid.append(row[2])
                self.buy_time.append(row[3])
                self.money.append(row[4])
        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
            return
        db.close()  # 关闭数据库连接

    def next_page(self):
        if self.page <= 1999:
            # 清除当前页数据
            self.id.clear()
            self.gid.clear()
            self.uid.clear()
            self.buy_time.clear()
            self.money.clear()

            # 页码加1
            self.page += 1

            # 获取下一页数据
            self.search_data()

            # 清除表格
            self.delButton()

            # 添加新页的数据
            for i in range(min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 插入数据
                self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

            for col in self.columns:  # 绑定函数，使表头可排序
                self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    def first_page(self):
        # 清除当前页数据
        self.id.clear()
        self.gid.clear()
        self.uid.clear()
        self.buy_time.clear()
        self.money.clear()

        # 页码加1
        self.page = 0

        # 获取下一页数据
        self.search_data()

        # 清除表格
        self.delButton()

        # 添加新页的数据
        for i in range(min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 插入数据
            self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    def last_page(self):
        # 清除当前页数据
        self.id.clear()
        self.gid.clear()
        self.uid.clear()
        self.buy_time.clear()
        self.money.clear()

        # 页码加1
        self.page = 1999

        # 获取下一页数据
        self.search_data()

        # 清除表格
        self.delButton()

        # 添加新页的数据
        for i in range(min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 插入数据
            self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    def previous_page(self):
        if self.page > 0:  # 如果不是第一页
            # 清除当前页数据
            self.id.clear()
            self.gid.clear()
            self.uid.clear()
            self.buy_time.clear()
            self.money.clear()

            # 页码减1
            self.page -= 1

            # 获取上一页数据
            self.search_data()

            # 清除表格
            self.delButton()

            # 添加新页的数据
            for i in range(
                    min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 插入数据
                self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

            for col in self.columns:  # 绑定函数，使表头可排序
                self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    # 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()  # 先将表格内的内容全部清空

        # print(self.chaxun.get())	# 输入框内的内容
        # 打开数据库连接，准备查找指定的信息
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        condition = ''
        if self.var_id.get() != '':
            if condition == '':
                condition = condition + 'id = ' + "\'" + self.var_id.get() + "\'"
            else:
                condition = condition + ' and id = ' + "\'" + self.var_id.get() + "\'"
        if self.var_gid.get() != '':
            if condition == '':
                condition = condition + 'gid = ' + "\'" + self.var_gid.get() + "\'"
            else:
                condition = condition + ' and gid = ' + "\'" + self.var_gid.get() + "\'"
        if self.var_uid.get() != '':
            if condition == '':
                condition = condition + 'uid = ' + "\'" + self.var_uid.get() + "\'"
            else:
                condition = condition + ' and uid = ' + "\'" + self.var_uid.get() + "\'"
        if self.var_buy_time.get() != '':
            if condition == '':
                condition = condition + 'buy_time = ' + "\'" + self.var_buy_time.get() + "\'"
            else:
                condition = condition + ' and buy_time = ' + "\'" + self.var_buy_time.get() + "\'"
        if self.var_money.get() != '':
            if condition == '':
                condition = condition + 'money = ' + "\'" + self.var_money.get() + "\'"
            else:
                condition = condition + ' and money = ' + "\'" + self.var_money.get() + "\'"
        sql = "SELECT * FROM t_order where " + condition
        print(sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            # 再次进行初始化，进行首行数据的插入
            self.id = []
            self.gid = []
            self.uid = []
            self.buy_time = []
            self.money = []
            # 向表格中插入数据
            for row in results:
                self.id.append(row[0])
                self.gid.append(row[1])
                self.uid.append(row[2])
                self.buy_time.append(row[3])
                self.money.append(row[4])

        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
            return
            db.close()  # 关闭数据库连接

        for i in range(min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    # 清空表格中的所有信息
    def delButton(self):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
        self.id1 = self.var_id.get()
        print(self.id1)
        self.var_gid.set(self.row_info[1])
        self.var_uid.set(self.row_info[2])
        self.var_buy_time.set(self.row_info[3])
        self.var_money.set(self.row_info[4])
        self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id,
                                        font=('Verdana', 15))

        print('')

    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def new_row(self):
        print(self.var_id.get())
        print(self.id)
        if str(self.var_id.get()) in self.id:
            messagebox.showinfo('警告！', '该商品已存在！')
        else:
            if self.var_id.get() != '' and self.var_gid.get() != '' and self.var_uid.get() != '' and self.var_buy_time.get() != '' and self.var_money.get() != '':
                # 打开数据库连接
                db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33",
                                      port=26000)
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "INSERT INTO t_order(id, gid, uid, buy_time, money) \
				       VALUES ('%s', '%s', '%s', '%s', '%s')" % \
                      (self.var_id.get(), self.var_gid.get(), self.var_uid.get(), self.var_buy_time.get(),
                       self.var_money.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    return
                db.close()  # 关闭数据库连接

                self.id.append(self.var_id.get())
                self.gid.append(self.var_gid.get())
                self.uid.append(self.var_uid.get())
                self.buy_time.append(self.var_buy_time.get())
                self.money.append(self.var_money.get())
                self.tree.insert('', len(self.id) - 1, values=(
                    self.id[len(self.id) - 1], self.gid[len(self.id) - 1], self.uid[len(self.id) - 1],
                    self.buy_time[len(self.id) - 1], self.money[len(self.id) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写订单信息')

    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
            # 打开数据库连接
            db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "UPDATE t_order SET id = '%s', gid = '%s', uid = '%s', buy_time = '%s', money = '%s' \
				where id = '%s'" % (
            self.var_id.get(), self.var_gid.get(), self.var_uid.get(), self.var_buy_time.get(), self.var_money.get(),
            self.id1)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
                return
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            self.gid[id_index] = self.var_gid.get()
            self.uid[id_index] = self.var_uid.get()
            self.buy_time[id_index] = self.var_buy_time.get()
            self.money[id_index] = self.var_money.get()

            self.tree.item(self.tree.selection()[0], values=(
                self.var_id.get(), self.var_gid.get(), self.var_uid.get(),
                self.var_buy_time.get(), self.var_money.get()))  # 修改对于行信息

    # 删除行
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的学号
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
            # 打开数据库连接
            db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "DELETE FROM t_order WHERE id = '%s'" % (self.row_info[0])  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
                return
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            print(id_index)
            del self.id[id_index]
            del self.gid[id_index]
            del self.uid[id_index]
            del self.buy_time[id_index]
            del self.money[id_index]
            print(self.id)
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())

# 用户菜单界面
class UserMenu:
    def __init__(self, parent_window, login_id):
        parent_window.destroy()  # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('信息管理界面')
        self.window.geometry('300x410+500+100')
        label = Label(self.window, text="请选择需要进行的操作", font=("Verdana", 20))
        label.pack(pady=100)  # pady=100 界面的长度

        Button(self.window, text="商品信息查看", font=tkFont.Font(size=16), width=30, height=2,
               command=lambda: UserGoods(self.window, login_id),
               fg='black', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="个人信息管理", font=tkFont.Font(size=16), width=30, height=2,
               command=lambda: UserInfo(self.window, login_id),
               fg='black', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="订单信息管理", font=tkFont.Font(size=16), width=30, height=2,
               command=lambda: UserOrder(self.window, login_id),
               fg='black', bg='gray', activebackground='black', activeforeground='white').pack()

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口

# 用户商品查看界面
class UserGoods:
    def __init__(self, parent_window, login_id):
        parent_window.destroy()  # 自动销毁上一个界面
        self.window = Tk()  # 初始框的声明
        self.window.title('管理员操作界面')
        self.window.geometry("650x685+300+30")  # 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=500, height=200)  # 指定框架，在窗口上可以显示，这里指定四个框架
        self.frame_center = tk.Frame(width=500, height=350)
        self.frame_bottom = tk.Frame(width=650, height=70)

        # 定义下方中心列表区域
        self.columns = ("商品id", "商品名称", "库存量")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 定义id1为修改id时的暂存变量，这个是为了更新信息而设计的
        self.id1 = 0

        # 表格的标题
        self.tree.column("商品id", width=int(500/3), anchor='center')
        self.tree.column("商品名称", width=int(500/3), anchor='center')
        self.tree.column("库存量", width=int(500/3), anchor='center')

        # grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        # 定义几个数组，为中间的那个大表格做一些准备
        self.id = []
        self.name = []
        self.price = []

        # 打开数据库连接
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_goods"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.name.append(row[1])
                self.price.append(row[2])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        print("test***********************")
        for i in range(min(len(self.id), len(self.name), len(self.price))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.name[i], self.price[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="商品信息:", font=('Verdana', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)  # NSEW表示允许组件向4个方向都可以拉伸

        # 定义下方区域
        self.chaxun = StringVar()
        self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=70, pady=20)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_id = StringVar()  # 声明学号
        self.var_name = StringVar()  # 声明姓名
        self.var_price = StringVar()  # 声明性别
        # 商品id
        self.right_top_id_label = Label(self.frame_left_top, text="商品id： ", font=('Verdana', 15))
        self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 15), state=DISABLED)
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
        # 商品名称
        self.right_top_name_label = Label(self.frame_left_top, text="商品名称：", font=('Verdana', 15))
        self.right_top_name_entry = Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 15), state=DISABLED)
        self.right_top_name_label.grid(row=2, column=0)  # 位置设置
        self.right_top_name_entry.grid(row=2, column=1)
        # 库存量
        self.right_top_gender_label = Label(self.frame_left_top, text="库存量：", font=('Verdana', 15))
        self.right_top_gender_entry = Entry(self.frame_left_top, textvariable=self.var_price, font=('Verdana', 15), state=DISABLED)
        self.right_top_gender_label.grid(row=3, column=0)  # 位置设置
        self.right_top_gender_entry.grid(row=3, column=1)

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)

        # 定义下方区域，查询功能块
        self.chaxun = StringVar()
        self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=20, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)

        # 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        # 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", lambda: self.back(login_id))  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

    # 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()  # 先将表格内的内容全部清空

        # print(self.chaxun.get())	# 输入框内的内容
        # 打开数据库连接，准备查找指定的信息
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM proc_cha('%s');" % (self.chaxun.get())
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            # 再次进行初始化，进行首行数据的插入
            self.id = []
            self.name = []
            self.price = []
            # 向表格中插入数据
            for row in results:
                self.id.append(row[0])
                self.name.append(row[1])
                self.price.append(row[2])

        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
            return
            db.close()  # 关闭数据库连接

        print("进行数据的插入")
        for i in range(min(len(self.id), len(self.name), len(self.price))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.name[i], self.price[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    # 清空表格中的所有信息
    def delButton(self):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

    # 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
        self.id1 = self.var_id.get()
        self.var_name.set(self.row_info[1])
        self.var_price.set(self.row_info[2])
        self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id,
                                        font=('Verdana', 15))

    # 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def back(self, login_id):
        UserMenu(self.window, login_id)  # 进入管理员子菜单操作界

# 用户信息操作界面
class UserInfo:
    def __init__(self, parent_window, login_id):
        parent_window.destroy()  # 销毁主界面

        self.window = Tk()  # 初始框的声明
        self.window.title('用户操作界面')
        self.window.geometry("1000x300+300+200")  # 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=600, height=250)
        self.frame_right_top = tk.Frame(width=400, height=200)

        self.id1 = None

        self.id = []
        self.passwd = []
        self.name = []
        self.number = []
        self.addr = []
        self.type = []
        # 打开数据库连接
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_user WHERE id = '%s'" % (login_id)  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id1 = row[0]
                self.id.append(row[0])
                self.passwd.append(row[1])
                self.name.append(row[2])
                self.number.append(row[3])
                self.addr.append(row[4])
                self.type.append(row[5])
        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="用户信息:", font=('Verdana', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=200, pady=10)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_id = StringVar()  # 声明学号
        self.var_passwd = StringVar()
        self.var_name = StringVar()  # 声明姓名
        self.var_number = StringVar()
        self.var_addr = StringVar()
        self.var_type = StringVar()

        # 设置各量的数值
        self.var_id.set(self.id[0])
        self.var_passwd.set(self.passwd[0])
        self.var_name.set(self.name[0])
        self.var_number.set(self.number[0])
        self.var_addr.set(self.addr[0])
        self.var_type.set(self.type[0])
        # id
        self.right_top_id_label = Label(self.frame_left_top, text="用户id：", font=('Verdana', 15))
        self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 15), state=DISABLED)
        self.right_top_id_label.grid(row=1, column=0, padx=100)  # 位置设置
        self.right_top_id_entry.grid(row=1, column=1)
        # passwd
        self.right_top_passwd_label = Label(self.frame_left_top, text="用户密码：", font=('Verdana', 15))
        self.right_top_passwd_entry = Entry(self.frame_left_top, textvariable=self.var_passwd, font=('Verdana', 15))
        self.right_top_passwd_label.grid(row=2, column=0)  # 位置设置
        self.right_top_passwd_entry.grid(row=2, column=1)
        # name
        self.right_top_name_label = Label(self.frame_left_top, text="姓名：", font=('Verdana', 15))
        self.right_top_name_entry = Entry(self.frame_left_top, textvariable=self.var_name,
                                            font=('Verdana', 15))
        self.right_top_name_label.grid(row=3, column=0)  # 位置设置
        self.right_top_name_entry.grid(row=3, column=1)
        # number
        self.right_top_number_label = Label(self.frame_left_top, text="电话：", font=('Verdana', 15))
        self.right_top_number_entry = Entry(self.frame_left_top, textvariable=self.var_number,
                                            font=('Verdana', 15))
        self.right_top_number_label.grid(row=4, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=4, column=1)
        # addr
        self.right_top_addr_label = Label(self.frame_left_top, text="地址：", font=('Verdana', 15))
        self.right_top_addr_entry = Entry(self.frame_left_top, textvariable=self.var_addr,
                                            font=('Verdana', 15))
        self.right_top_addr_label.grid(row=5, column=0)  # 位置设置
        self.right_top_addr_entry.grid(row=5, column=1)
        # type
        self.right_top_type_label = Label(self.frame_left_top, text="类型：", font=('Verdana', 15))
        self.right_top_type_entry = Entry(self.frame_left_top, textvariable=self.var_type,
                                            font=('Verdana', 15), state=DISABLED)
        self.right_top_type_label.grid(row=6, column=0)  # 位置设置
        self.right_top_type_entry.grid(row=6, column=1)

        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 20))

        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新用户信息', width=20,
                                            command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='注销用户', width=20,
                                            command=self.del_row)

        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单
        self.frame_right_top.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", lambda: self.back(login_id))  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环


    def back(self, login_id):
        UserMenu(self.window, login_id)  # 进入管理员子菜单操作界面

    # 更新数据及表格
    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
            # 打开数据库连接
            db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "UPDATE t_user SET id = '%s', passwd = '%s', name = '%s', number = '%s', addr = '%s', type = '%s' \
				where id = '%s'" % (
            self.var_id.get(), self.var_passwd.get(), self.var_name.get(), self.var_number.get(), self.var_addr.get(), self.var_type.get(), self.id1)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
                return
            db.close()  # 关闭数据库连接

            self.id[0] = self.var_id.get()
            self.passwd[0] = self.var_passwd.get()
            self.name[0] = self.var_name.get()
            self.number[0] = self.var_number.get()
            self.addr[0] = self.var_addr.get()
            self.type[0] = self.var_type.get()

    # 删除行
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            # 打开数据库连接
            db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            print(self.var_id.get())
            sql = """
            DELETE FROM t_order WHERE uid = '%s';
            DELETE FROM t_user WHERE id = '%s';
            """ % (self.var_id.get(), self.var_id.get())  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
                return
            db.close()  # 关闭数据库连接

            del self.id[0]
            del self.passwd[0]
            del self.name[0]
            del self.number[0]
            del self.addr[0]
            del self.type[0]
            print(self.id)

            StartPage(self.window)

# 订单信息操作界面
class UserOrder:
    def __init__(self, parent_window, login_id):
        parent_window.destroy()  # 销毁主界面

        self.window = Tk()  # 初始框的声明
        self.window.geometry("650x720+300+30")  # 初始窗口在屏幕中的位置
        self.window.title('用户操作界面')

        self.frame_left_top = tk.Frame(width=300, height=230)
        self.frame_right_top = tk.Frame(width=200, height=230)
        self.frame_center = tk.Frame(width=500, height=360)
        self.frame_bottom = tk.Frame(width=650, height=60)

        self.id1 = 0

        # 定义下方中心列表区域
        self.columns = ("订单id", "商品id", "用户id", "订单创建时间", "订单量")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("订单id", width=100, anchor='center')  # 表示列,不显示
        self.tree.column("商品id", width=100, anchor='center')
        self.tree.column("用户id", width=100, anchor='center')
        self.tree.column("订单创建时间", width=100, anchor='center')
        self.tree.column("订单量", width=100, anchor='center')

        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.id = []
        self.gid = []
        self.uid = []
        self.buy_time = []
        self.money = []
        self.page = 0  # 初始化页数
        self.limit = 500  # 数据量限制
        # 打开数据库连接
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_order WHERE uid = '%s' LIMIT 500" % (login_id)  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.gid.append(row[1])
                self.uid.append(row[2])
                self.buy_time.append(row[3])
                self.money.append(row[4])
        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        print("test***********************")
        for i in range(min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="订单信息:", font=('Verdana', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_id = StringVar()  # 声明商品id
        self.var_gid = StringVar()  # 声明订单id
        self.var_uid = StringVar()  # 声明订单创建时间
        self.var_buy_time = StringVar()  # 声明订单是否成功交易
        self.var_money = StringVar()  # 声明交易金额

        self.right_top_id_label = Label(self.frame_left_top, text="订单id： ", font=('Verdana', 15))
        self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 15))
        self.right_top_id_label.grid(row=1, column=0)  # 位置设置
        self.right_top_id_entry.grid(row=1, column=1)

        self.right_top_gid_label = Label(self.frame_left_top, text="商品id：", font=('Verdana', 15))
        self.right_top_gid_entry = Entry(self.frame_left_top, textvariable=self.var_gid, font=('Verdana', 15))
        self.right_top_gid_label.grid(row=2, column=0)  # 位置设置
        self.right_top_gid_entry.grid(row=2, column=1)

        self.right_top_uid_label = Label(self.frame_left_top, text="用户id：", font=('Verdana', 15))
        self.right_top_uid_entry = Entry(self.frame_left_top, textvariable=self.var_uid, font=('Verdana', 15), state=DISABLED)
        self.right_top_uid_label.grid(row=3, column=0)  # 位置设置
        self.right_top_uid_entry.grid(row=3, column=1)

        self.right_top_buy_time_label = Label(self.frame_left_top, text="订单创建时间：", font=('Verdana', 15))
        self.right_top_buy_time_entry = Entry(self.frame_left_top, textvariable=self.var_buy_time, font=('Verdana', 15))
        self.right_top_buy_time_label.grid(row=4, column=0)  # 位置设置
        self.right_top_buy_time_entry.grid(row=4, column=1)

        self.right_top_money_label = Label(self.frame_left_top, text="订单量：", font=('Verdana', 15))
        self.right_top_money_entry = Entry(self.frame_left_top, textvariable=self.var_money, font=('Verdana', 15))
        self.right_top_money_label.grid(row=5, column=0)  # 位置设置
        self.right_top_money_entry.grid(row=5, column=1)

        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 20))

        self.tree.bind('<Button-1>', self.info)  # 左键获取位置
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建订单信息', width=15, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中订单信息', width=15,
                                            command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中订单信息', width=15,
                                            command=self.del_row)
        self.right_top_button4 = ttk.Button(self.frame_right_top, text='查询', width=15,
                                            command=self.put_data)

        # 定义下方区域
        # 设置第一页和最后一页按钮
        self.first_button = ttk.Button(self.frame_bottom, text='第一页', command=lambda: self.first_page(login_id))
        self.first_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
        # 设置下页和上页按钮
        self.next_button = ttk.Button(self.frame_bottom, text='下一页', command=lambda: self.next_page(login_id))
        self.previous_button = ttk.Button(self.frame_bottom, text='上一页', command=lambda: self.previous_page(login_id))
        self.next_button.grid(row=0, column=1, padx=20, pady=20)  # 位置设置
        self.previous_button.grid(row=0, column=2, padx=20, pady=20)  # 位置设置
        # 设置重置按钮
        self.reset_button = ttk.Button(self.frame_bottom, text='重置', command=lambda: self.first_page(login_id))
        self.reset_button.grid(row=0, column=4, padx=20, pady=20)  # 位置设置

        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
        self.right_top_button4.grid(row=5, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", lambda: self.back(login_id))  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self, login_id):
        UserMenu(self.window, login_id)  # 进入管理员子菜单操作界面

    def info(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
        self.id1 = self.var_id.get()
        print(self.id1)
        self.var_gid.set(self.row_info[1])
        self.var_uid.set(self.row_info[2])
        self.var_buy_time.set(self.row_info[3])
        self.var_money.set(self.row_info[4])

        var_uname = StringVar()
        var_gname = StringVar()

        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = """
        SELECT t_user.name, t_goods.name
        FROM t_user, t_goods
        WHERE t_user.id = '%s' AND t_goods.id = '%s'
        """ % (self.var_uid.get(), self.var_gid.get()) # SQL 插入语句
        try:
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
            results = cursor.fetchall()
            for row in results:
                var_uname.set(row[0])
                var_gname.set(row[1])
        except:
            db.rollback()  # 发生错误时回滚
            messagebox.showinfo('警告！', '查询失败，数据库连接失败！')
            return
        db.close()  # 关闭数据库连接

        newwindow = Toplevel()  # 初始框的声明
        newwindow.grab_set()
        newwindow.focus()
        newwindow.title('详情')
        newwindow.geometry("600x300+300+200")  # 初始窗口在屏幕中的位置

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(newwindow, text="订单信息:", font=('Verdana', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=200, pady=10)
        # id
        self.right_top_id_label = Label(newwindow, text="订单id：", font=('Verdana', 15))
        self.right_top_id_entry = Entry(newwindow, textvariable=self.var_id, font=('Verdana', 15),
                                        state=DISABLED)
        self.right_top_id_label.grid(row=1, column=0, padx=100)  # 位置设置
        self.right_top_id_entry.grid(row=1, column=1)
        # gid
        self.right_top_gid_label = Label(newwindow, text="商品id：", font=('Verdana', 15))
        self.right_top_gid_entry = Entry(newwindow, textvariable=self.var_gid, font=('Verdana', 15), state=DISABLED)
        self.right_top_gid_label.grid(row=2, column=0)  # 位置设置
        self.right_top_gid_entry.grid(row=2, column=1)
        # gname
        self.right_top_gname_label = Label(newwindow, text="商品名称：", font=('Verdana', 15))
        self.right_top_gname_entry = Entry(newwindow, textvariable=var_gname, font=('Verdana', 15), state=DISABLED)
        self.right_top_gname_label.grid(row=3, column=0)  # 位置设置
        self.right_top_gname_entry.grid(row=3, column=1)
        # uid
        self.right_top_uid_label = Label(newwindow, text="用户id：", font=('Verdana', 15))
        self.right_top_uid_entry = Entry(newwindow, textvariable=self.var_uid,
                                          font=('Verdana', 15), state=DISABLED)
        self.right_top_uid_label.grid(row=4, column=0)  # 位置设置
        self.right_top_uid_entry.grid(row=4, column=1)
        # uname
        self.right_top_uname_label = Label(newwindow, text="用户姓名：", font=('Verdana', 15))
        self.right_top_uname_entry = Entry(newwindow, textvariable=var_uname,
                                          font=('Verdana', 15), state=DISABLED)
        self.right_top_uname_label.grid(row=5, column=0)  # 位置设置
        self.right_top_uname_entry.grid(row=5, column=1)
        # buy_time
        self.right_top_buy_time_label = Label(newwindow, text="创建时间：", font=('Verdana', 15))
        self.right_top_buy_time_entry = Entry(newwindow, textvariable=self.var_buy_time,
                                            font=('Verdana', 15), state=DISABLED)
        self.right_top_buy_time_label.grid(row=6, column=0)  # 位置设置
        self.right_top_buy_time_entry.grid(row=6, column=1)
        # money
        self.right_top_money_label = Label(newwindow, text="订单量：", font=('Verdana', 15))
        self.right_top_money_entry = Entry(newwindow, textvariable=self.var_money,
                                          font=('Verdana', 15), state=DISABLED)
        self.right_top_money_label.grid(row=7, column=0)  # 位置设置
        self.right_top_money_entry.grid(row=7, column=1)


        # 整体区域定位
        newwindow.grid(row=0, column=0, padx=2, pady=5)

        newwindow.grid_propagate(0)

        newwindow.tkraise()  # 开始显示主菜单

    def search_data(self, login_id):
        # 打开数据库连接
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_order WHERE uid = %s LIMIT %d OFFSET %d" % ("\'" + login_id + "\'", self.limit, self.limit * self.page)  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.id.append(row[0])
                self.gid.append(row[1])
                self.uid.append(row[2])
                self.buy_time.append(row[3])
                self.money.append(row[4])
        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
            return
        db.close()  # 关闭数据库连接

    def next_page(self, login_id):
        if self.page <= 1999:
            # 清除当前页数据
            self.id.clear()
            self.gid.clear()
            self.uid.clear()
            self.buy_time.clear()
            self.money.clear()

            # 页码加1
            self.page += 1

            # 获取下一页数据
            self.search_data(login_id)

            # 清除表格
            self.delButton()

            # 添加新页的数据
            for i in range(min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 插入数据
                self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

            for col in self.columns:  # 绑定函数，使表头可排序
                self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
    def first_page(self, login_id):
        # 清除当前页数据
        self.id.clear()
        self.gid.clear()
        self.uid.clear()
        self.buy_time.clear()
        self.money.clear()

        # 页码加1
        self.page = 0

        # 获取下一页数据
        self.search_data(login_id)

        # 清除表格
        self.delButton()

        # 添加新页的数据
        for i in range(min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 插入数据
            self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    def last_page(self, login_id):
        # 清除当前页数据
        self.id.clear()
        self.gid.clear()
        self.uid.clear()
        self.buy_time.clear()
        self.money.clear()

        # 页码加1
        self.page = 1999

        # 获取下一页数据
        self.search_data(login_id)

        # 清除表格
        self.delButton()

        # 添加新页的数据
        for i in range(min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 插入数据
            self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    def previous_page(self, login_id):
        if self.page > 0:  # 如果不是第一页
            # 清除当前页数据
            self.id.clear()
            self.gid.clear()
            self.uid.clear()
            self.buy_time.clear()
            self.money.clear()

            # 页码减1
            self.page -= 1

            # 获取上一页数据
            self.search_data(login_id)

            # 清除表格
            self.delButton()

            # 添加新页的数据
            for i in range(
                    min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 插入数据
                self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

            for col in self.columns:  # 绑定函数，使表头可排序
                self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    # 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()  # 先将表格内的内容全部清空

        # print(self.chaxun.get())	# 输入框内的内容
        # 打开数据库连接，准备查找指定的信息
        db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        condition = ''
        if self.var_id.get() != '':
            if condition == '':
                condition = condition + 'id = ' + "\'" + self.var_id.get() + "\'"
            else:
                condition = condition + ' and id = ' + "\'" + self.var_id.get() + "\'"
        if self.var_gid.get() != '':
            if condition == '':
                condition = condition + 'gid = ' + "\'" + self.var_gid.get() + "\'"
            else:
                condition = condition + ' and gid = ' + "\'" + self.var_gid.get() + "\'"
        if self.var_uid.get() != '':
            if condition == '':
                condition = condition + 'uid = ' + "\'" + self.var_uid.get() + "\'"
            else:
                condition = condition + ' and uid = ' + "\'" + self.var_uid.get() + "\'"
        if self.var_buy_time.get() != '':
            if condition == '':
                condition = condition + 'buy_time = ' + "\'" + self.var_buy_time.get() + "\'"
            else:
                condition = condition + ' and buy_time = ' + "\'" + self.var_buy_time.get() + "\'"
        if self.var_money.get() != '':
            if condition == '':
                condition = condition + 'money = ' + "\'" + self.var_money.get() + "\'"
            else:
                condition = condition + ' and money = ' + "\'" + self.var_money.get() + "\'"
        sql = "SELECT * FROM t_order where " + condition
        print(sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()

            # 再次进行初始化，进行首行数据的插入
            self.id = []
            self.gid = []
            self.uid = []
            self.buy_time = []
            self.money = []
            # 向表格中插入数据
            for row in results:
                self.id.append(row[0])
                self.gid.append(row[1])
                self.uid.append(row[2])
                self.buy_time.append(row[3])
                self.money.append(row[4])

        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
            return
            db.close()  # 关闭数据库连接

        for i in range(min(len(self.id), len(self.gid), len(self.uid), len(self.buy_time), len(self.money))):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.gid[i], self.uid[i], self.buy_time[i], self.money[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

    # 清空表格中的所有信息
    def delButton(self):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
        self.id1 = self.var_id.get()
        print(self.id1)
        self.var_gid.set(self.row_info[1])
        self.var_uid.set(self.row_info[2])
        self.var_buy_time.set(self.row_info[3])
        self.var_money.set(self.row_info[4])
        self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id,
                                        font=('Verdana', 15))

        print('')

    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def new_row(self):
        print(self.var_id.get())
        print(self.id)
        if str(self.var_id.get()) in self.id:
            messagebox.showinfo('警告！', '该订单已存在！')
        else:
            if self.var_id.get() != '' and self.var_gid.get() != '' and self.var_uid.get() != '' and self.var_buy_time.get() != '' and self.var_money.get() != '':
                # 打开数据库连接
                db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33",
                                      port=26000)
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "INSERT INTO t_order(id, gid, uid, buy_time, money) \
				       VALUES ('%s', '%s', '%s', '%s', '%s')" % \
                      (self.var_id.get(), self.var_gid.get(), self.var_uid.get(), self.var_buy_time.get(),
                       self.var_money.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    return
                db.close()  # 关闭数据库连接

                self.id.append(self.var_id.get())
                self.gid.append(self.var_gid.get())
                self.uid.append(self.var_uid.get())
                self.buy_time.append(self.var_buy_time.get())
                self.money.append(self.var_money.get())
                self.tree.insert('', len(self.id) - 1, values=(
                    self.id[len(self.id) - 1], self.gid[len(self.id) - 1], self.uid[len(self.id) - 1],
                    self.buy_time[len(self.id) - 1], self.money[len(self.id) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写订单信息')

    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
            # 打开数据库连接
            db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "UPDATE t_order SET id = '%s', gid = '%s', uid = '%s', buy_time = '%s', money = '%s' \
				where id = '%s'" % (
            self.var_id.get(), self.var_gid.get(), self.var_uid.get(), self.var_buy_time.get(), self.var_money.get(),
            self.id1)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
                return
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            self.gid[id_index] = self.var_gid.get()
            self.uid[id_index] = self.var_uid.get()
            self.buy_time[id_index] = self.var_buy_time.get()
            self.money[id_index] = self.var_money.get()

            self.tree.item(self.tree.selection()[0], values=(
                self.var_id.get(), self.var_gid.get(), self.var_uid.get(),
                self.var_buy_time.get(), self.var_money.get()))  # 修改对于行信息

    # 删除行
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的学号
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
            # 打开数据库连接
            db = psycopg2.connect(database="db_rzy", user="rzy", password="Rzy021006", host="1.92.80.33", port=26000)
            cursor = db.cursor()  # 使用cursor()方法获取操作游标
            sql = "DELETE FROM t_order WHERE id = '%s'" % (self.row_info[0])  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
                return
            db.close()  # 关闭数据库连接

            id_index = self.id.index(self.row_info[0])
            print(id_index)
            del self.id[id_index]
            del self.gid[id_index]
            del self.uid[id_index]
            del self.buy_time[id_index]
            del self.money[id_index]
            print(self.id)
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())

if __name__ == '__main__':
    # 实例化Application
    window = tk.Tk()
    StartPage(window)
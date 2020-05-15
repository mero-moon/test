# -*- coding:utf-8 *-
# description: ECC 椭圆曲线加密算法实现

# 获取y的负元
def get_inverse(mu, p):
    for i in range(1, p):
        if (i*mu)%p == 1:
            return i
    return -1

# 获取最大公约数
def get_gcd(zi, mu):
    if mu:
        return get_gcd(mu, zi%mu)
    else:
        return zi

#  获取 n*p，每次+p，直到求解阶数 np=-p 
def get_np(x1, y1, x2, y2, a, p):
    flag = 1
    if x1 == x2 and y1 == y2:
        zi = 3 * (x1 ** 2) + a
        mu = 2 * y1
    else:
        zi = y2 - y1
        mu = x2 - x1
        if zi * mu < 0:
            flag = 0
            zi = abs(zi) 
            mu = abs(mu)
    gcd_value = get_gcd(zi, mu)
    zi = zi // gcd_value
    mu = mu // gcd_value
    inverse_value = get_inverse(mu, p)
    k = (zi * inverse_value)
    if flag == 0:
        k = -k
    k = k % p 
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return x3, y3

# 获取椭圆曲线的阶
def get_rank(x0, y0, a, b, p):
    x1 = x0
    y1 = (-1*y0)%p
    tempX = x0
    tempY = y0
    n = 1
    while True:
        n += 1
        p_x,p_y = get_np(tempX, tempY, x0, y0, a, p)
        if p_x == x1 and p_y == y1:
            return n+1
        tempX = p_x
        tempY = p_y

# 计算p与-p
def get_param(x0, a, b, p):
    y0 = -1
    for i in range(p):
        if i**2%p == (x0**3 + a*x0 + b)%p:
            y0 = 1
            break
    if y0 == -1:
        return False
    x1 = x0
    y1 = (-1*y0) % p
    return x0,y0,x1,y1

# 输出椭圆曲线散点图
def get_graph(a, b, p):
    x_y = []
    for i in range(p):
        x_y.append(['-' for i in range(p)])
    for i in range(p):
        val =get_param(i, a, b, p)
        if(val != False):
            x0,y0,x1,y1 = val
            x_y[x0][y0] = 1
            x_y[x1][y1] = 1
    print("椭圆曲线的散列图为：")
    for i in range(p):
        temp = p-1-i
        if(temp >= 10):
            print(temp, end=" ")
        else:
            print(temp, end="  ")
        for j in range(p):
            print(x_y[j][temp], end="  ")
        print("")
    print("  ", end="")
    for i in range(p):
        if i >=10:
            print(i, end=" ")
        else:
            print(i, end="  ")
    print('\n')

# 计算nG
def get_ng(G_x, G_y, key, a, p):
    temp_x = G_x
    temp_y = G_y
    while(key != 1):
        temp_x,temp_y = get_np(temp_x,temp_y, G_x, G_y, a, p)
        key -= 1
    return temp_x,temp_y

def ecc_main():
    while True:
        a = int(input("请输入椭圆曲线参数 a(a>0)的值："))
        b = int(input("请输入椭圆曲线参数 b(b>0)的值："))
        p = int(input("请输入椭圆曲线参数 p(p 为素数)的值："))
        if (4*(a**3)+27*(b**2))%p == 0:
            print("您输入的参数有误，请重新输入！！！\n")
        else:
            break

    get_graph(a, b, p)

    print("user1：在如上坐标系中选一个值为 G 的坐标")
    G_x = int(input("user1：请输入选取的 x 坐标值："))
    G_y = int(input("user1：请输入选取的 y 坐标值："))
    n = get_rank(G_x, G_y, a, b, p)
    key = int(input("user1：请输入私钥小 key（<{}）： ".format(n)))
    KEY_x,kEY_y = get_ng(G_x, G_y, key, a, p)

    #user2
    k = int(input("user2：请输入一个整数 k（<{}）用于求 kG 和 kQ： ".format(n)))
    k_G_x,k_G_y = get_ng(G_x, G_y, k, a, p)
    k_Q_x,k_Q_y = get_ng(KEY_x, kEY_y, k, a, p)

    #加密
    plain_text = input("user2：请输入需要加密的字符串:")
    plain_text = plain_text.strip()
    c = []
    print("密文为：",end="")
    for char in plain_text:
        intchar = ord(char)
        cipher_text = intchar*k_Q_x
        c.append([k_G_x, k_G_y, cipher_text])
        print("({},{}),{}".format(k_G_x, k_G_y, cipher_text),end="-")
    
    #user1
    print("\nuser1 解密得到明文：",end="")
    for charArr in c:
        decrypto_text_x,decrypto_text_y = get_ng(charArr[0], charArr[1], key, a, p)
        print(chr(charArr[2]//decrypto_text_x),end="")
    
if __name__ == "__main__":
    print("*************ECC 椭圆曲线加密*************")
    ecc_main()


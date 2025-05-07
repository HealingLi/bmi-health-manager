#计算BMI指数
#BMI = 体重 / （身高**2）
user_Height = float(input("Please enter your Height(m):"))
user_Weight = float(input("Please enter your Weight(kg):"))
user_BMI = user_Weight / (user_Height) ** 2
print("Your BMI is " + str(user_BMI)) 
 

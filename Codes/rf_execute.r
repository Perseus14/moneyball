library("e1071")
library("randomForest")
d = read.table("out1",stringsAsFactors = FALSE)
for(i in 1:dim(d)[1])
{
result = tryCatch(
	{
 data <- read.csv(paste("./Data/Processed/Defenders/",d[i,1],sep=""))

no_rows <- nrow(data)
#choose features for model
features <- data[23:45]
features <- cbind(features, data[57])
features <- subset(features, select = -c(saves, penalties_saved))

y <- data[58]
#z score standardization of features
features <- scale(features)
#head(features)
#removing NaN features
#dim(features)
#sapply(features, class)
features1 <- features[,colSums(is.nan(features))<nrow(features)]
#head(features1)
#choose rows
row=features1[no_rows,]
features1 <- features1[1 : (no_rows-1), ]
y <- y[1 : (no_rows-1), ]
#convert y from integer to numeric
y <- sapply(y, as.numeric)
#TODO:find actual average points for M cut
y <- cut(y, c(-1, 2, 4, 100), labels=c("L", "M", "H"))
features1=data.frame(features1)
features=data.frame(features)
y=data.frame(y)
z=cbind(features1,y)


#define test and train data percentage
z[,"train"] <- ifelse(runif(nrow(z)) < 0.70, 1, 0)
train_col_num <- grep("train", names(z))
train_data <- z[z$train == 1, -train_col_num]
test_data <- z[z$train == 0, -train_col_num]

#tune the SVM by choosing best parameters
#svm_tune <- tune(svm, train.features=train_data, train.y=y, kernel="radial", ranges=list(cost=10^(-1:2), gamma=c(.5,1,2)))

#choose model with best parameters
#svm_model <- svm(as.factor(y) ~ .,data=train_data, kernel="radial")# cost=svm_tune$best.parameters$cost, gamma=svm_tune$best.parameters$gamma)
rf_model<-randomForest(as.factor(y) ~ .,data=train_data)

pred <- predict(rf_model, features[no_rows,])
vals=cbind(data[1,1],as.character(pred))
#print(data[1,1])
#print(as.character(pred))
print(as.character(vals))

	}, error = function(e) 
	{
	#print(paste("error",d[i,1]))
	#print(paste("MY_ERROR:  ",e))
	#print(svm_model)
	})


#summary(svm_model)
}

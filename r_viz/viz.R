library("ggplot2")

getwd()
setwd("/Users/anishpradhan/Projects/2019/surya_back")

data = read.csv("data/team_results.csv")
data <- subset(data, team == 'liv' | team == 'tot' | team == 'mc' | team == 'mu'| team == 'che' | team == 'ars')
# data$match_id = as.factor(data$match_id)
data$date = as.POSIXlt(data$date)
month_sort <- c(8,9,10,11,12,1,2,3,4,5,6,7)
month_order <- month.abb[month_sort]
data$month = factor(months(data$date, abbreviate = TRUE),levels=month_order)
data$month.abb <- data$month.abb


ggplot(data, aes(match_id,total,  group = team)) + 
  scale_y_continuous(sec.axis = dup_axis(), breaks=seq(0, 90, 6))+
  scale_x_continuous(limits = c(1, 32), breaks=seq(1,32,1)) +
  geom_line(aes(colour = team),size=1)+
  geom_point(aes(color=team, shape=team),size=1.5)+
  scale_shape_manual(values=seq(0,11)) +
  scale_color_manual(values=c("#FF0000","#0A4595","#D3171E","#2259A1","#D20222","#0F204B"))+
  # scale_color_manual(values=c("#FF0000","#001FFD","#70193D","#0000E7","#0A4595","#090808","#3899D7","#D3171E","#2259A1","#D20222","#D71920","#0F204B"))+
  xlab("Match Day") + ylab("Total Points")+
  geom_ribbon(aes(ymin = -Inf, ymax = Inf, fill = month, group = month), alpha = .2)



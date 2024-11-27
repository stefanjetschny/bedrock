data1m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_1m_50Hz');
data2m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_2m_30Hz');
data3m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_3m_30Hz');
data4m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_4m_30Hz');
data5m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_5m_30Hz');
data6m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_6m_30Hz');
data7m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_7m_30Hz');
data8m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_8m_30Hz');
data9m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_9m_50Hz');
data10m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_10m_30Hz');
data11m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_11m_30Hz');
data12m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_12m_30Hz');
data13m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_13m_30Hz');
data14m=wavread('C:\Users\sjet\OneDrive - NILU\projets\2021_bedrock\Onsøy\one_set_14m_30Hz');


dataT1=data1m
dataT2=data2m
dataT3=data3m
dataT4=data4m
dataT5=data5m
dataT6=data6m
dataT7=data7m
dataT8=data8m

//dataT1=data8m
//dataT2=data9m
//dataT3=data10m
//dataT4=data11m
//dataT5=data12m
//dataT6=data13m
//dataT7=data14m
//dataT8=data14m


//legend_string=['8 m', '9 m', '10 m', '11 m','12 m','13 m','14 m'];

legend_string=['1 m', '2 m', '3 m','4 m','5 m','6 m','7 m','8 m'];

xdel(winsid())

[no_traces, no_samples]= size(data1m);
sampling_rate=1/(no_samples);
t= 0:sampling_rate:(sampling_rate)*(no_samples-1);

figure(1)
// seismogram style. offset vs. time
// raw data
//plot(t,data1m(:,2)+1,'-r')
//plot(t,data2m(:,2)+2,'-g')
//plot(t,data3m(:,2)+3,'-b')
//plot(t,data4m(:,2)+4,'-c')
//plot(t,data5m(:,2)+5,'-y')
//plot(t,data6m(:,2)+6,'-m')
//plot(t,data7m(:,2)+7,'-k')

trace2plot=1

plot(t,dataT1(trace2plot,:)./max(dataT1(trace2plot,:))+1,'-r')
plot(t,dataT2(trace2plot,:)./max(dataT2(trace2plot,:))+2,'-g')
plot(t,dataT3(trace2plot,:)./max(dataT3(trace2plot,:))+3,'-b')
plot(t,dataT4(trace2plot,:)./max(dataT4(trace2plot,:))+4,'-c')
plot(t,dataT5(trace2plot,:)./max(dataT5(trace2plot,:))+5,'-y')
plot(t,dataT6(trace2plot,:)./max(dataT6(trace2plot,:))+6,'-m')
plot(t,dataT7(trace2plot,:)./max(dataT7(trace2plot,:))+7,'-k')
plot(t,dataT8(trace2plot,:)./max(dataT8(trace2plot,:))+8,'-r')

legend(legend_string);


ax=gca() ;//get the current axes  
ax.box="on";  
//ax.data_bounds=[0,-.2;0.25,0.2];  //define the bounds  
ylabel("amplitude", "fontsize", 3, "color", "black");
xlabel("time in s", "fontsize", 3, "color", "black");

ax.font_size=2

figure(2)
// trace style. traces overlay
// raw data

//plot(t,data1m(:,2)./max(data1m(:,2))+1,'-r')
//plot(t,data2m(:,2)./max(data2m(:,2))+2,'-g')
//plot(t,data3m(:,2)./max(data3m(:,2))+4,'-b')
//plot(t,data4m(:,2)./max(data4m(:,2))+4,'-y')
//plot(t,data5m(:,2)./max(data5m(:,2))+5,'-m')
//
//legend('1 m', '2 m', '3 m','4 m','5 m','6 m','7 m');
//
//ax=gca() ;//get the current axes  
//ax.box="on";  
//ax.data_bounds=[0,-1.1;0.25,1.1];  //define the bounds  
//ylabel("amplitude", "fontsize", 3, "color", "black");
//xlabel("time in s", "fontsize", 3, "color", "black");
//
//ax.font_size=2

plot(t,dataT1(trace2plot,:),'-r')
plot(t,dataT2(trace2plot,:),'-g')
plot(t,dataT3(trace2plot,:),'-b')
plot(t,dataT4(trace2plot,:),'-c')
plot(t,dataT5(trace2plot,:),'-y')
plot(t,dataT6(trace2plot,:),'-m')
plot(t,dataT7(trace2plot,:),'-k')
plot(t,dataT8(trace2plot,:),'-r')

legend(legend_string);

ax=gca() ;//get the current axes  
ax.box="on";  
//ax.data_bounds=[0,-.2;0.25,0.2];  //define the bounds  
ylabel("amplitude", "fontsize", 3, "color", "black");
xlabel("time in s", "fontsize", 3, "color", "black");

ax.font_size=2


Order   = 5; // The order of the filter
Fs      = 1/sampling_rate; // The sampling frequency
Fcutoff = 50;   // The cutoff frequency
hz = iir(Order,'lp','butt',[Fcutoff/Fs 0],[0.1 0.1])
dataT1_filt = flts(dataT1(trace2plot,:),hz);
dataT2_filt = flts(dataT2(trace2plot,:),hz);
dataT3_filt = flts(dataT3(trace2plot,:),hz);
dataT4_filt = flts(dataT4(trace2plot,:),hz);
dataT5_filt = flts(dataT5(trace2plot,:),hz);
dataT6_filt = flts(dataT6(trace2plot,:),hz);
dataT7_filt = flts(dataT7(trace2plot,:),hz);
dataT8_filt = flts(dataT8(trace2plot,:),hz);

figure(3)
// seismogram style. offset vs. time
// filtered data
plot(t,dataT1_filt./max(dataT1_filt)+1,'-r')
plot(t,dataT2_filt./max(dataT2_filt)+2,'-g')
plot(t,dataT3_filt./max(dataT3_filt)+3,'-b')
plot(t,dataT4_filt./max(dataT4_filt)+4,'-c')
plot(t,dataT5_filt./max(dataT5_filt)+5,'-y')
plot(t,dataT6_filt./max(dataT6_filt)+6,'-m')
plot(t,dataT7_filt./max(dataT7_filt)+7,'-k')
plot(t,dataT8_filt./max(dataT8_filt)+8,'-r')
legend(legend_string);

ax=gca() ;//get the current axes  
ax.box="on";  
//ax.data_bounds=[0.0,1;0,9];  //define the bounds  
ylabel("amplitude", "fontsize", 3, "color", "black");
xlabel("time in s", "fontsize", 3, "color", "black");

figure(4)
// trace style. traces overlay
// filered data
plot(t,dataT1_filt./max(dataT1_filt),'-r')
plot(t,dataT2_filt./max(dataT2_filt),'-g')
plot(t,dataT3_filt./max(dataT3_filt),'-b')
plot(t,dataT4_filt./max(dataT4_filt),'-c')
plot(t,dataT5_filt./max(dataT5_filt),'-y')
plot(t,dataT6_filt./max(dataT6_filt),'-m')
plot(t,dataT7_filt./max(dataT7_filt),'-k')
plot(t,dataT8_filt./max(dataT8_filt),'-r')
legend(legend_string);

ax=gca() ;//get the current axes  
ax.box="on";  
//ax.data_bounds=[0.09,-0.15;0.135,0.15];  //define the bounds  
ylabel("amplitude", "fontsize", 3, "color", "black");
xlabel("time in s", "fontsize", 3, "color", "black");



figure(5)
// trace style. traces overlay
// single trace, filtered and raw trace overlay 
plot(t,dataT1(trace2plot,:)./max(dataT1(trace2plot,:)),'-r')
//plot(t,data1m(:,2),'-g')
//plot(t,data1m(:,1)./max(data1m(:,1)),'--b')
plot(t,dataT1_filt./max(dataT1_filt),'--b')
legend('channel 1', 'channel 1 filt');

ax=gca() ;//get the current axes  
//ax.box="on";  
//ax.data_bounds=[0.09,-0.15;0.135,0.15];  //define the bounds  
ylabel("amplitude", "fontsize", 3, "color", "black");
xlabel("time in s", "fontsize", 3, "color", "black");

dataT1_spec = abs(fft(dataT1(trace2plot,:)));
dataT1_filt_spec = abs(fft(dataT1_filt));

figure(6)
plot(dataT1_spec(1:(no_samples/2)),'-r')
plot(dataT1_filt_spec(1:(no_samples/2)),'--b')
ax=gca() ;//get the current axes  
ax.box="on";  
ax.data_bounds=[0,0;500,1000];  //define the bounds  
ylabel("Amplitude", "fontsize", 3, "color", "black");
xlabel("Frequency in Hz", "fontsize", 3, "color", "black");
legend('channel 1', 'channel 1 filt');

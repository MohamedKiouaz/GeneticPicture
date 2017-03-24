clc
close all
clear all

pkg load image

%1.jpg Rectangles.png TPS.jpg Tigre.jpg
filename = "1.jpg";
savefile = strcat(filename,'.mat');

img = imread(filename);
if(size(size(img), 2) == 3)
    img = rgb2gray(img);
end

[c d] = size(img);

P = 2;
Generations = 1000;
N = 800;
nb_enfants = 3;

if(exist(savefile, 'file') == 2)
    load(savefile)
else
    people = ones(P, N, 5);
    people(:, :, 3:4) = 5;
    D = [];
end

figure(1)

subplot(2, 2, 1)
imshow(img)

img_clean = ones([c d], 'uint8') .* mean(mean(img));

for i=0:Generations
    [a b] = size(people);
    for j=1:nb_enfants*a
        x_temp = people(mod(j, a) + 1, :, :);
        x_temp = reshape(x_temp, N, 5);
        img3 = img_clean;
        for k=1:N
           img3(x_temp(k, 1):x_temp(k, 3), x_temp(k, 2):x_temp(k, 4)) = x_temp(k, 5);
        end
        for k=1:N
            if(rand() < 1/N/4)
                l = randi(50) + 10;
                x_temp(k, 1) = randi(c - l);
                x_temp(k, 2) = randi(d - l);
                x_temp(k, 3:4) = x_temp(k, 1:2) + l;
                x_temp(k, 5) = randi(256) - 1;
            end
        end
        img2 = img_clean;
        for k=1:N
           img2(x_temp(k, 1):x_temp(k, 3), x_temp(k, 2):x_temp(k, 4)) = x_temp(k, 5);
        end
        f = sum(sum(abs(int16(img3) - int16(img))));
        if(sum(sum(abs(int16(img2) - int16(img)))) < f)
            people(mod(j,a)+1, :, :) = x_temp;
            D = [D f];
        end
    end
    if(mod(i, 20) == 0)
        subplot(2, 2, 2)
        imshow(img3)
        title(strcat("Distance=", num2str(f)))
        
        subplot(2, 2, [3 4])
        if(size(D, 2) > 1000 && mod(size(D, 2), 2) == 0)
            D = mean([D(1, 1:2:end)', D(1, 2:2:end)'], 2)';
        end
        plot(D)
        
        save(savefile, 'people', 'D');
        pause(0.001)
    end
end
